from ibapi.client import *
from ibapi.wrapper import *
import time
import threading

class TestApp(EClient, EWrapper):
  def __init__(self):
    EClient.__init__(self, self)
  
  def nextValidId(self, orderId):
    self.orderId = orderId
  
  def nextId(self):
    self.orderId += 1
    return self.orderId

  def error(self, reqId, errorCode, errorString, advancedOrderReject, errorTime):
    print(f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, orderReject: {advancedOrderReject}, errorTime: {errorTime}")

  def contractDetails(self, reqId, contractDetails):
    attrs = vars(contractDetails)
    # print("\n".join(f"{name}: {value}" for name,value in attrs.items()))
    print(contractDetails.contract)

  def contractDetailsEnd(self, reqId):
    print("End of contract details")
    self.disconnect()

app = TestApp()
app.connect("127.0.0.1", 7497, clientId=0)
threading.Thread(target=app.run).start()
time.sleep(1)

mycontract = Contract()

# Stock
# mycontract.symbol = "AAPL"
# mycontract.secType = "STK"
# mycontract.currency = "USD"
# mycontract.exchange = "SMART"
# mycontract.primaryExchange = "NASDAQ"

# Future
# mycontract.symbol = "ES"
# mycontract.secType = "FUT"
# mycontract.currency = "USD"
# mycontract.exchange = "CME"
# mycontract.lastTradeDateOrContractMonth = "202512"

# Option
mycontract.symbol = "SPX"
mycontract.secType = "OPT"
mycontract.currency = "USD"
mycontract.exchange = "SMART"
mycontract.lastTradeDateOrContractMonth = "202511"
mycontract.right = "P" # put or call option
mycontract.tradingClass = "SPXW" # monthly/weekly options denoted by last letter
mycontract.strike = 5300

app.reqContractDetails(app.nextId(), mycontract)
