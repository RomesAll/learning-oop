from order import DiscountCalculation, RegularDiscount, VipDiscount

if __name__ == '__main__':
    total_reg = RegularDiscount().apply(total=100)
    total_vip = VipDiscount().apply(total=100)
    print(f'reg: {total_reg}\nvip: {total_vip}')