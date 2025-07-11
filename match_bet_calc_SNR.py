def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print("❌ Value must be zero or greater.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


def calculate_net_profits(back_stake, back_odds, lay_odds, back_comm, lay_comm, lay_stake):
    # Back win
    back_profit = (back_odds - 1) * back_stake * (1 - back_comm)
    liability = (lay_odds - 1) * lay_stake
    net_back_win = back_profit - liability

    # Lay win
    lay_profit = lay_stake * (1 - lay_comm)
    net_lay_win = lay_profit - back_stake

    return net_back_win, net_lay_win, liability


def calculate_net_profits_snr(free_bet_amount, back_odds, lay_odds, back_comm, lay_comm, lay_stake):
    # Back win (no stake returned)
    back_profit = (back_odds - 1) * free_bet_amount * (1 - back_comm)
    liability = (lay_odds - 1) * lay_stake
    net_back_win = back_profit - liability

    # Lay win
    lay_profit = lay_stake * (1 - lay_comm)
    net_lay_win = lay_profit

    return net_back_win, net_lay_win, liability


def find_balanced_lay_stake(back_stake, back_odds, lay_odds, back_comm, lay_comm, snr_mode=False):
    if snr_mode:
        approx_lay_stake = ((back_odds - 1) * back_stake * (1 - back_comm)) / (lay_odds * (1 - lay_comm))
    else:
        approx_lay_stake = (back_odds * back_stake * (1 - back_comm)) / (lay_odds * (1 - lay_comm))

    low = approx_lay_stake * 0.8
    high = approx_lay_stake * 1.2

    tolerance = 0.001
    max_iterations = 40
    iteration = 0

    while iteration < max_iterations:
        mid = (low + high) / 2
        if snr_mode:
            net_back_win, net_lay_win, _ = calculate_net_profits_snr(
                back_stake, back_odds, lay_odds, back_comm, lay_comm, mid)
        else:
            net_back_win, net_lay_win, _ = calculate_net_profits(
                back_stake, back_odds, lay_odds, back_comm, lay_comm, mid)

        diff = net_back_win - net_lay_win

        if abs(diff) < tolerance:
            return mid

        if diff > 0:
            low = mid
        else:
            high = mid

        iteration += 1

    return (low + high) / 2


def matched_bet_balanced_loss():
    print("Matched Bet Calculator\n")
    print("Select bet type:")
    print("1. Normal bet (qualifying)")
    print("2. Free bet (SNR - stake not returned)")
    bet_type = input("Enter 1 or 2: ")

    snr_mode = bet_type.strip() == "2"

    if snr_mode:
        back_stake = get_positive_float("Enter free bet amount (£): ")
    else:
        back_stake = get_positive_float("Enter back stake (£): ")

    back_odds = get_positive_float("Enter back odds: ")
    lay_odds = get_positive_float("Enter lay odds: ")
    back_comm = get_positive_float("Enter bookmaker commission (%) (usually 0): ") / 100
    lay_comm = get_positive_float("Enter exchange commission (%) (e.g. 5): ") / 100

    lay_stake = find_balanced_lay_stake(back_stake, back_odds, lay_odds, back_comm, lay_comm, snr_mode)

    if snr_mode:
        net_back_win, net_lay_win, liability = calculate_net_profits_snr(
            back_stake, back_odds, lay_odds, back_comm, lay_comm, lay_stake
        )
    else:
        net_back_win, net_lay_win, liability = calculate_net_profits(
            back_stake, back_odds, lay_odds, back_comm, lay_comm, lay_stake
        )

    # Output
    print("\n--- Results ---")
    print(f"Lay stake: £{lay_stake:.2f}")
    print(f"Liability at exchange: £{liability:.2f}")
    print(f"Profit/loss if back bet wins: £{net_back_win:.2f}")
    print(f"Profit/loss if lay bet wins: £{net_lay_win:.2f}")


# Run the calculator
matched_bet_balanced_loss()