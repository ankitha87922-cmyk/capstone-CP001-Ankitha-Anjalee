public class BankAccount {

    private String accountNumber;
    private String customerName;
    private String accountType;
    private double balance;


    public BankAccount(String accountNumber, String customerName,
                       String accountType, double balance) {
        this.accountNumber = accountNumber;
        this.customerName = customerName;
        this.accountType = accountType;
       this.balance = balance;
    }
}


