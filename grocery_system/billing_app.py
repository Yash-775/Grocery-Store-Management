import tkinter as tk
from tkinter import ttk, messagebox
import django
import os
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grocery_system.settings")
django.setup()

from store.models import Product, Order, OrderItem, Employee, Customer  # include Customer

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing System")

        self.selected_items = []
        self.total_amount = 0

        self.create_widgets()

    def create_widgets(self):
        # Customer name input
        tk.Label(self.root, text="Customer Name:").grid(row=0, column=0)
        self.customer_name_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.customer_name_var).grid(row=0, column=1)

        # Product selection
        tk.Label(self.root, text="Select Product").grid(row=1, column=0)
        self.product_var = tk.StringVar()
        self.product_menu = ttk.Combobox(self.root, textvariable=self.product_var)
        self.product_menu['values'] = [f"{p.name} (\u20B9{p.price})" for p in Product.objects.all()]
        self.product_menu.grid(row=1, column=1)

        # Quantity
        tk.Label(self.root, text="Quantity").grid(row=2, column=0)
        self.qty_entry = tk.Entry(self.root)
        self.qty_entry.grid(row=2, column=1)

        # Add button
        tk.Button(self.root, text="Add Item", command=self.add_item).grid(row=3, column=0, columnspan=2, pady=5)

        # Bill list
        self.item_list = tk.Text(self.root, height=10, width=40)
        self.item_list.grid(row=4, column=0, columnspan=2, pady=10)

        # Total
        self.total_label = tk.Label(self.root, text="Total: \u20B90")
        self.total_label.grid(row=5, column=0, columnspan=2)

        # Generate Bill
        tk.Button(self.root, text="Generate Bill", command=self.generate_bill).grid(row=6, column=0, columnspan=2)

    def add_item(self):
        product_name = self.product_var.get().split(" (")[0]
        try:
            quantity = int(self.qty_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid quantity")
            return

        product = Product.objects.filter(name=product_name).first()
        if not product:
            messagebox.showerror("Error", "Product not found")
            return
        if quantity > product.quantity:
            messagebox.showerror("Error", f"Only {product.quantity} items in stock.")
            return

        subtotal = quantity * product.price
        self.total_amount += subtotal

        self.selected_items.append((product, quantity, subtotal))
        self.item_list.insert(tk.END, f"{product.name} x {quantity} = \u20B9{subtotal}\n")
        self.total_label.config(text=f"Total: \u20B9{self.total_amount}")

        # Reset input
        self.qty_entry.delete(0, tk.END)
        self.product_var.set('')

    def generate_bill(self):
        if not self.selected_items:
            messagebox.showwarning("Warning", "Add items before billing")
            return

        customer_name = self.customer_name_var.get().strip()
        if not customer_name:
            messagebox.showwarning("Warning", "Please enter customer name")
            return

        customer, _ = Customer.objects.get_or_create(name=customer_name)
        employee = Employee.objects.first()  # You may improve this with session handling later

        order = Order.objects.create(customer=customer, employee=employee, total_amount=self.total_amount)

        for product, quantity, subtotal in self.selected_items:
            OrderItem.objects.create(order=order, product=product, quantity=quantity, subtotal=subtotal)
            product.quantity -= quantity
            product.save()

        messagebox.showinfo("Success", f"Order #{order.id} placed successfully!")

        self.item_list.delete(1.0, tk.END)
        self.selected_items.clear()
        self.total_amount = 0
        self.total_label.config(text="Total: \u20B90")
        self.customer_name_var.set('')

# Run app
if __name__ == '__main__':
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
