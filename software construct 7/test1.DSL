@startuml
' 枚举类型定义
enum OrderStatus {
    CREATE
    PAID
    SHIPPING
    DELIVERED
    CANCEL
}

' 类定义
class Customer {
    - name: String
    - contact: String
    - deliveryAddress: String
    - active: boolean
}

class Order {
    - createDate: Date
    - status: OrderStatus
}

class OrderDetail {
    - quantity: int
    + calculateSubTotal(): double
    + calculateWeight(): double
}

class Product {
    - title: String
    - weight: double
    - description: String
    + getPriceForQuantity(): double
    + getWeight(): double
}

abstract class Payment {
    - amount: double
}

class Credit {
    - number: String
    - type: String
    - expireDate: Date
}

class Cash {
    - cashTendered: double
}

class WireTransfer {
    - bankID: String
    - bankName: String
}

class AliPay {
    - number: String
}

class WeixinPay {
    - number: String
}

' 关系定义
Customer "1" --> "0..*" Order
Order "1" *--> "1..*" OrderDetail
OrderDetail "1" --> "1" Product
Order "1" --> "1" Payment

Payment <|-- Credit
Payment <|-- Cash
Payment <|-- WireTransfer
Payment <|-- AliPay
Payment <|-- WeixinPay

' 添加注释说明
note top of Payment
  支付方式支持五种类型：
  - 信用卡(Credit)
  - 现金(Cash)
  - 在线转账(WireTransfer)
  - 支付宝(AliPay)
  - 微信支付(WeixinPay)
end note

note right of OrderDetail
  方法说明：
  - calculateSubTotal(): 计算小计
  - calculateWeight(): 计算重量
end note
@enduml