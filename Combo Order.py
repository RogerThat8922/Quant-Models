from ibapi.client import *
from ibapi.wrapper import *
from ibapi.contract import ComboLeg
from ibapi.tag_value import TagValue

port = 7497
clientId = 0 

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        # Order info
        mycontract = Contract()
        mycontract.symbol = "AAPL,TSLA"
        mycontract.secType = "BAG"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        leg1 = ComboLeg()
        leg1.conId = 76792991 #Tesla
        leg1.ratio = 1
        leg1.action = "BUY"
        leg1.exchange = "SMART"

        leg2 = ComboLeg()
        leg2.conId = 265598 #Apple
        leg2.ratio = 1
        leg2.action = "SELL"
        leg2.exchange = "SMART"

        mycontract.comboLegs = []
        mycontract.comboLegs.append(leg1)
        mycontract.comboLegs.append(leg2)

        myorder = Order()
        myorder.orderId = orderId
        myorder.action = "SELL"
        myorder.orderType = "LMT"
        myorder.lmtPrice = 80
        myorder.totalQuantity = 10
        myorder.tif = "GTC"
        myorder.smartComboRoutingParams = []
        myorder.smartComboRoutingParams.append(TagValue('NonGuaranteed', '1'))

        self.placeOrder(orderId, mycontract, myorder)


    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"orderId: {orderId}, contract: {contract}, order: {order}, Maintenance Margin: {orderState.maintMarginChange}")

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderStatus. orderId: {orderId}, status:  {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"execDetails. reqId: {reqId}, contract: {contract}, execution:  {execution}")

app = TestApp()
app.connect("127.0.0.1", port, clientId)
app.run()