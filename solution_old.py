import datetime
from tkinter import *
import tkinter.scrolledtext as tkst
#Kalpesh Doshi
class CDSell:

	def __init__(self, window):

		self.window = window

		#dictionary to the list of lists (data holding)
		self.cd_data = {}
		self.customer_addresses = {}

		self.labelCustomerName = Label(self.window, text="Customer Name:", fg='black', borderwidth=2)
		self.labelCustomerAddress = Label(self.window, text="Customer Address:", fg='black', borderwidth=2)

		self.entryCustomerName = Entry(self.window, width=40)
		self.entryCustomerAddress = Entry(self.window, width=40)

		self.labelCustomerName.grid(row=1, column=0)
		self.labelCustomerAddress.grid(row=2, column=0)
		self.entryCustomerName.grid(row=1, column=1)
		self.entryCustomerAddress.grid(row=2, column=1)


		self.labelCDName = Label(self.window, text="CD Title", fg='black', borderwidth=2)
		self.labelCDName.grid(row=4, column=0)
		self.cdOptions = ["Lucy Nelson's Greatest Hits", "Barry Cuda & The Sharks LIVE",
		"Busta Move Boogies"]

		self.cdPrices = {"Lucy Nelson's Greatest Hits":9.99, "Barry Cuda & The Sharks LIVE":26.99,
		"Busta Move Boogies":29.99}

		self.cdVar = StringVar(self.window)
		self.cdVar.set(self.cdOptions[0])

		self.opt = OptionMenu(self.window, self.cdVar, *self.cdOptions)
		self.opt.config(width=40)
		self.opt.grid(row=4,column=1)
		self.cdVar.trace('w',self.update_cost)


		self.labelCDCost = Label(self.window, text="CD Unit cost", fg='black', borderwidth=2)
		self.labelCDCost.grid(row=5,column=0)
		self.labelCDCostVal = Label(self.window, text="$" + str(self.cdPrices[self.cdVar.get()]), fg='black', borderwidth=2)
		self.labelCDCostVal.grid(row=5,column=1)

		self.labelQuantity = Label(self.window, text="Quantity:", fg='black', borderwidth=2)
		self.entryQuantity = Entry(self.window, width=20)

		self.labelQuantity.grid(row=6, column=0)
		self.entryQuantity.grid(row=6, column=1)

		self.addBtn = Button(self.window, text="Add Order", command=self.add)
		self.displayBtn = Button(self.window, text="Display All", command=self.display)
		self.clearBtn = Button(self.window, text="Clear", command=self.onClear)

		self.addBtn.grid(row=8,column=1,sticky='W',pady=10)
		self.displayBtn.grid(row=8,column=1,pady=10)
		self.clearBtn.grid(row=8,column=1,sticky='E',pady=10)

		self.textArea = tkst.ScrolledText(master=self.window, wrap = WORD, width = 100, height=20)
		self.textArea.grid(row=10,column=0,columnspan=5)


	def update_cost(self, *a):
		self.labelCDCostVal['text'] = "$" + str(self.cdPrices[self.cdVar.get()])

	def add(self):
		customerName = self.entryCustomerName.get()
		customerAddress = self.entryCustomerAddress.get()

		if customerName not in self.cd_data:
			self.cd_data[customerName] = []
			self.customer_addresses[customerName] = customerAddress


		#cd Title, quantity, date
		dataList = []
		dataList.append(self.cdVar.get())
		dataList.append(int(self.entryQuantity.get()))
		dataList.append(datetime.datetime.now())

		self.cd_data[customerName].append(dataList)


	def display(self):
		# print(self.cd_data)
		
		totalProfit = 0
		for key, value in self.cd_data.items():

			self.textArea.insert(INSERT, "Name: %s\nAddress: %s\n" % (key, self.customer_addresses[key]))			
			self.textArea.insert(INSERT, "CDs Bought\n")
			totalSubTotal = 0
			self.textArea.insert(INSERT, "%-20s %-30s %-9s %-9s %-6s %-9s\n" % ("Date", "CD Title", "U.Cost", "R.Price", "Qty", "Sub.T"))
			for l in value:
				retailPrice = self.cdPrices[l[0]] * 1.4 #40% + UC
				
				totalProfit += 0.4*self.cdPrices[l[0]]

				self.textArea.insert(INSERT, "%-20s %-30s $%-8.2f $%-8.2f x%-5d " % (l[2].strftime("%m/%d/%Y, %H:%M:%S"), l[0], self.cdPrices[l[0]], retailPrice, l[1]))
				subtotal = retailPrice*l[1]
				totalSubTotal += subtotal
				self.textArea.insert(INSERT, "$%-8.2f\n" % (subtotal))

			salesTax = 0.06 * totalSubTotal
			self.textArea.insert(INSERT, "SALES TAX: $%.2f\n" % (salesTax))
			shippingCharges = 0

			if (totalSubTotal < 40):
				shippingCharges = 15.00
			elif (totalSubTotal < 150):
				shippingCharges = 10

			if (shippingCharges == 0):
				self.textArea.insert(INSERT, "Shipping Charges: FREE\n")
			else:
				self.textArea.insert(INSERT, "Shipping Charges: $%.2f\n" % (shippingCharges))

			orderTotal = salesTax + totalSubTotal + shippingCharges
			self.textArea.insert(INSERT, "[*] Order Total: $%.2f\n" % (orderTotal))
			self.textArea.insert(INSERT, "\n")

			self.textArea.yview(END)

		self.textArea.insert(INSERT, "[+] Total PROFIT earned: $%.2f\n" % (totalProfit))


	def onClear(self):
		self.textArea.delete('1.0', END)
		self.entryCustomerName.delete("0", END)
		self.entryCustomerAddress.delete("0", END)


window = Tk()

window.title("CD Sell")
obj = CDSell(window)

window.mainloop()