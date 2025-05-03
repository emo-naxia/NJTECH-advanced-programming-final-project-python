import os
import time
from datetime import datetime

MENU_FILE = "menu.txt"


class MenuItem:
    def __init__(self, number, name, price, discount):
        self.number = number
        self.name = name
        self.price = price
        self.discount = discount

    def display(self):
        print(f"{self.number} | {self.name} | ¥{self.price} | 折扣: {self.discount}")

    def to_line(self):
        return f"{self.number} {self.name} {self.price} {self.discount}"


def load_menu():
    menu = []
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 4:
                    number, name, price, discount = parts
                    menu.append(MenuItem(number, name, float(price), float(discount)))
    return menu


def save_menu(menu):
    with open(MENU_FILE, "w") as f:
        for item in menu:
            f.write(item.to_line() + "\n")


def admin_menu():
    menu = load_menu()
    while True:
        print("\n--- 管理员功能菜单 ---")
        print("1. 添加菜品")
        print("2. 修改菜品")
        print("3. 删除菜品")
        print("4. 查询菜品")
        print("5. 保存菜单")
        print("0. 返回主菜单")
        choice = input("选择操作: ")

        if choice == "1":
            name = input("菜名: ")
            price = float(input("价格: "))
            discount = float(input("折扣（1表示无折扣）: "))
            number = str(1000 + len(menu) + 1)
            menu.append(MenuItem(number, name, price, discount))
            print("添加成功！")
        elif choice == "2":
            code = input("输入菜品编号: ")
            found = False
            for item in menu:
                if item.number == code:
                    item.name = input("新名称: ")
                    item.price = float(input("新价格: "))
                    item.discount = float(input("新折扣: "))
                    print("修改成功！")
                    found = True
                    break
            if not found:
                print("未找到该编号菜品。")
        elif choice == "3":
            code = input("输入菜品编号: ")
            menu = [item for item in menu if item.number != code]
            print("删除成功（如果编号存在）！")
        elif choice == "4":
            keyword = input("请输入编号或名称: ")
            found = False
            for item in menu:
                if item.number == keyword or item.name == keyword:
                    item.display()
                    found = True
            if not found:
                print("未找到该菜品。")
        elif choice == "5":
            save_menu(menu)
            print("菜单已保存。")
        elif choice == "0":
            break
        else:
            print("无效操作。")


def customer_order():
    menu = load_menu()
    if not menu:
        print("菜单为空，请联系管理员添加菜品。")
        return

    print("\n--- 当前菜单 ---")
    for item in menu:
        item.display()

    orders = []
    while True:
        code = input("请输入菜品编号（输入0结束）: ")
        if code == "0":
            break
        matched = next((m for m in menu if m.number == code), None)
        if matched:
            qty = int(input("请输入份数: "))
            orders.append((matched, qty))
        else:
            print("未找到该菜品。")

    if not orders:
        print("未点任何菜品，取消订单。")
        return

    all_total = sum(item.price * item.discount * qty for item, qty in orders)
    order_number = datetime.now().strftime("%Y%m%d%H%M%S")

    mode = input("请选择用餐方式（1. 堂食  2. 外卖）: ")
    if mode == "1":
        table = input("请输入桌号: ")
        box_fee = float(input("包厢费（无则输入0）: "))
        all_total += box_fee
        file = order_number + "_dinein.txt"
        with open(file, "w") as f:
            for item, qty in orders:
                f.write(f"{item.number} {item.name} {item.price} {item.discount} {qty}\n")
            f.write(f"桌号: {table} 包厢费: {box_fee} 总价: {all_total:.2f}\n")
    elif mode == "2":
        time = input("送餐时间（如18:00）: ")
        addr = input("送餐地址: ")
        phone = input("联系电话: ")
        fee = float(input("外卖费（无则输入0）: "))
        all_total += fee
        file = order_number + "_takeout.txt"
        with open(file, "w") as f:
            for item, qty in orders:
                f.write(f"{item.number} {item.name} {item.price} {item.discount} {qty}\n")
            f.write(f"送餐时间: {time} 地址: {addr} 电话: {phone} 外卖费: {fee} 总价: {all_total:.2f}\n")
    else:
        print("无效选择，订单取消。")
        return

    print(f"订单已生成：{file}")


def main():
    while True:
        print("\n=== 欢迎使用自助点单系统 ===")
        print("1. 管理员登录")
        print("2. 顾客点餐")
        print("0. 退出")
        choice = input("请选择操作: ")

        if choice == "1":
            user = input("账号: ")
            pwd = input("密码: ")
            if user == "admin" and pwd == "123456":
                admin_menu()
            else:
                print("账号或密码错误。")
        elif choice == "2":
            customer_order()
        elif choice == "0":
            print("感谢使用，再见！")
            break
        else:
            print("无效选择，请重试。")


if __name__ == "__main__":
    main()
