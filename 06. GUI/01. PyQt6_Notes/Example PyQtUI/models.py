from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
Base = declarative_base()


class VoucherNoModel(Base):
    __tablename__ = "voucher_model"  # Corrected table name
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incremented primary key
    voucher_no = Column(Integer, nullable=False, unique=True)  # Unique voucher number


# Seller Model
class SellerProfileModel(Base):
    __tablename__ = "seller_profile_model"
    id = Column(Integer, primary_key=True)
    seller_name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    seller_rank = Column(Integer, default=0)
    total_receivable = Column(Integer, default=0)
    total_get_paid_amount = Column(Integer, default=0)
    total_commission = Column(Integer, default=0)
    date = Column(Date)
    entry_by = Column(String, nullable=True)

    sellers = relationship("SellingModel", back_populates="seller_profile")

class SellingModel(Base):
    __tablename__ = "selling_model"
    id = Column(Integer, primary_key=True)
    vouchar_no = Column(String, nullable=False)
    seller_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    sell_amount = Column(Integer)
    commission_amount = Column(Integer, default=0)
    total_cost_amount = Column(Integer, default=0)
    entry_by = Column(String, nullable=True)

    category_id = Column(Integer, ForeignKey("seller_profile_model.id"))
    seller_profile = relationship("SellerProfileModel", back_populates="sellers")

# Buyer Model
class BuyerProfileModel(Base):
    __tablename__ = "buyer_profile_model"
    id = Column(Integer, primary_key=True)
    buyer_name = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    buyer_rank = Column(Integer, default=0)
    total_payable = Column(Integer, default=0)
    total_paid = Column(Integer, default=0)
    date = Column(Date)
    entry_by = Column(String, nullable=True)
    buyers = relationship("BuyingModel", back_populates="buyer_profile")

class BuyingModel(Base):
    __tablename__ = 'buying_model'
    id = Column(Integer, primary_key=True)
    vouchar_no = Column(String, nullable=False)
    buyer_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    fish_name = Column(String, nullable=True)
    fish_rate = Column(String)
    raw_weight = Column(String)
    final_weight = Column(String)
    buying_amount = Column(Integer)
    seller_name = Column(String, nullable=True)
    entry_by = Column(String, nullable=True)

    category_id = Column(Integer, ForeignKey("buyer_profile_model.id"))
    buyer_profile = relationship("BuyerProfileModel", back_populates="buyers")

# Dealer Model
class DealerModel(Base):
    __tablename__ = 'dealer_model'
    id = Column(Integer, primary_key=True)
    entry_name = Column(String, nullable=False)  # all_accounting, paid_to_seller, get_paid_from_buyer,
    # capital_withdrawal, capital_deposit, borrowing, loan_repayment,salary, other_cost, mosque, somiti, other_cost_voucher
    # giving_loan, receiving_loan
    name = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    paying_amount = Column(Integer, default=0)
    receiving_amount = Column(Integer, default=0)
    entry_by = Column(String, nullable=True)
    description = Column(String, nullable=True)


class LoanModel(Base):
    __tablename__ = 'loan_model'
    id = Column(Integer, primary_key=True)
    loan_payer_name = Column(String)
    date = Column(Date, nullable=False)
    amount = Column(Integer)
    entry_by = Column(String)

class PayingLoanModel(Base):
    __tablename__ = 'paying_loan_model'
    id = Column(Integer, primary_key=True)
    loan_receiver_name = Column(String)
    date = Column(Date, nullable=False)
    amount = Column(Integer)
    entry_by = Column(String)

class CostModel(Base):
    __tablename__ = 'cost_model'
    id = Column(Integer, primary_key=True, default=1)
    mosque = Column(Integer, default=0)
    mosque_get_paid = Column(Integer, default=0)
    somiti = Column(Integer, default=0)
    somiti_get_paid = Column(Integer, default=0)
    other_cost = Column(Integer, default=0)
    other_cost_paid = Column(Integer, default=0)

class SettingModel(Base):
    __tablename__ = 'setting_model'
    id = Column(Integer, primary_key=True, default=1)
    username = Column(String, default='admin')
    commission = Column(Float, default=4)
    dhol = Column(Integer, default=100)
    font = Column(String, default="Bangla")

class UserModel(Base):
    __tablename__ ='user_model'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, default='admin')
    password = Column(String, default='admin')
    role = Column(String, default='admin')
    delete = Column(Boolean, default=False)

# Final Accounting Model
class FinalAccounting(Base):
    __tablename__ = "final_accounting"
    id = Column(Integer, primary_key=True, default=1)
    capital = Column(Integer, default=0)
    # total capital, total loan, total received, total paid, total payable, total receivable,


# Create a new SQLite database and session
engine = create_engine('sqlite:///business.db')  # Use your preferred database URL
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Ensure FinalAccounting record exists and is initialized with zero
def initialize():
    accounting = session.query(FinalAccounting).first()
    if not accounting:
        accounting = FinalAccounting()
        session.add(accounting)
        session.commit()
    cost = session.query(CostModel).first()
    if not cost:
        cost = CostModel()
        session.add(cost)
        session.commit()
    setting = session.query(SettingModel).first()
    if not setting:
        setting = SettingModel()
        session.add(setting)
        session.commit()
    user = session.query(UserModel).first()
    if not user:
        user = UserModel()
        session.add(user)
        session.commit()
    session.close()
# Call the initialization function when the software runs
initialize()