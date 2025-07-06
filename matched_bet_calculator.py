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
    # back win
    back_profit = (back_odds - 1) * back_stake * (1 - back_comm)
    liability = (lay_odds - 1) * lay_stake
    net_back_win = back_profit - liability

    # lay win
    lay_profit = lay_stake * (1 - lay_comm)
    net_lay_win = lay_profit - back_stake

    return net_back_win, net_lay_win, liability


def find_balanced_lay_stake(back_stake, back_odds, lay_odds, back_comm, lay_comm):
    # Start with a reasonable range for lay stake
    low = 0
    high = back_stake * 5  # arbitrarily large

    tolerance = 0.0001
    while high - low > tolerance:
        mid = (low + high) / 2
        net_back_win, net_lay_win, _ = calculate_net_profits(back_stake, back_odds, lay_odds, back_comm, lay_comm, mid)
        diff = net_back_win - net_lay_win

        if abs(diff) < tolerance:
            return mid  # balanced!
        elif diff > 0:
            # back win is more profitable → increase lay stake
            low = mid
        else:
            # lay win is more profitable → decrease lay stake
            high = mid

    return (low + high) / 2


def matched_bet_balanced_loss():
    print("📊 Matched Bet Qualifying Loss Calculator (Numerical Balance)\n")

    # Inputs
    back_stake = get_positive_float("Enter back stake (£): ")
    back_odds = get_positive_float("Enter back odds: ")
    lay_odds = get_positive_float("Enter lay odds: ")
    back_comm = get_positive_float("Enter bookmaker commission (%) (usually 0): ") / 100
    lay_comm = get_positive_float("Enter exchange commission (%) (e.g. 5): ") / 100

    # Find lay stake that balances outcomes
    lay_stake = find_balanced_lay_stake(back_stake, back_odds, lay_odds, back_comm, lay_comm)
    net_back_win, net_lay_win, liability = calculate_net_profits(
        back_stake, back_odds, lay_odds, back_comm, lay_comm, lay_stake
    )

    average_loss = round((net_back_win + net_lay_win) / 2, 2)

    # Output
    print("\n--- Results ---")
    print(f"Lay stake (balanced): £{lay_stake:.2f}")
    print(f"Liability at exchange: £{liability:.2f}")
    print(f"Qualifying loss: £{abs(average_loss)}")
    print(f"Profit if back bet wins: £{net_back_win:.2f}")
    print(f"Profit if lay bet wins: £{net_lay_win:.2f}")


# Run the calculator
matched_bet_balanced_loss()