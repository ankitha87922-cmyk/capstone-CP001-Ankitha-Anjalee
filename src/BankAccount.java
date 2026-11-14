public class BankAccount {

    private String accountNumber;
    private String customerName;
    private String accountType;
    private double balance;

    private static int nextAccountNumber = 100001;

    public BankAccount(String customerName,
                       String accountType,
                       double openingDeposit) {

        this.accountNumber = String.valueOf(nextAccountNumber++);
        this.customerName = customerName;
        this.accountType = accountType;
        this.balance = openingDeposit;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    public String getCustomerName() {
        return customerName;
    }

    public String getAccountType() {
        return accountType;
    }

    public double getBalance() {
        return balance;
    }

    public void displayAccountDetails() {
        System.out.println("Account Number: " + accountNumber);
        System.out.println("Customer Name: " + customerName);
        System.out.println("Account Type: " + accountType);
        System.out.println("Balance: " + balance);
    }
}