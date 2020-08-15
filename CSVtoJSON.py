with open('orders.csv') as orders:
    orders_list = list()
    for line in orders:
        order = line.split(",")
        order_dict = {"Date": order[0].strip(),
                      "Item": order[1].strip(),
                      "Total": float(order[2].strip()),
                      "Members": {}}
        if order[3].strip() != "0":
            order_dict['Members']['Nishant'] = float(order[3].strip())
        if order[4].strip() != "0":
            order_dict['Members']['Arjun'] = float(order[4].strip())
        if order[5].strip() != "0":
            order_dict['Members']['Param'] = float(order[5].strip())
        orders_list.append(order_dict)
    print(orders_list)