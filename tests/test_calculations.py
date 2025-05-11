from app.calculations import add,Bank,Insuffiecent
import pytest



@pytest.fixture
def zero_bank_account():
    print("creating empty  bank account ")
    return Bank()
@pytest.fixture
def defined_bank_account():
    print("creating 50$  bank account ")
    return Bank(50)






@pytest.mark.parametrize("num1,num2,result",[
    (1,2,3),
    (9,1,10),
    (12,8,20)
])
def test_add(num1,num2,result):
    print("test1")
    assert add(num1,num2)==result


def test_initial_bank():
    assert Bank().balance==0

def test_deposit(zero_bank_account):
    zero_bank_account.deposit(30)
    
    assert zero_bank_account.balance==30

def test_withdrew(defined_bank_account):
    
    defined_bank_account.withdraw(30)
    assert defined_bank_account.balance==20

def test_transactions(zero_bank_account):
    with pytest.raises(Insuffiecent):
            zero_bank_account.withdraw(1)
               