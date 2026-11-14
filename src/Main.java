import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc=new Scanner(System.in);
        System.out.println("Welcome to VaultCore - Core Banking Transaction Engine!");
        System.out.println("========== VAULTCORE BANK ==========");
        System.out.println("1. Open New Account");
        System.out.println("2. Exit");
        System.out.print("Enter your choice: ");
        int choice = sc.nextInt();
        sc.nextLine();
        if (choice == 1) {
            System.out.print("Enter customer name: ");
            String customerName = sc.nextLine();
            while (customerName.trim().isEmpty()) {
                System.out.print("Name cannot be empty. Please enter customer name: ");
                customerName = sc.nextLine();
            }
            System.out.print("Enter account type (Savings/Current): ");
            String accountType = sc.nextLine();
            while (!accountType.equalsIgnoreCase("Savings") &&
                    !accountType.equalsIgnoreCase("Current")) {

                System.out.print("Invalid account type. Please enter Savings or Current: ");
                accountType = sc.nextLine();
            }

            System.out.print("Enter opening deposit: ");
            double openingDeposit = sc.nextDouble();
            while (openingDeposit < 0) {
                System.out.print("Invalid deposit! Please enter a positive amount: ");
                openingDeposit = sc.nextDouble();
            }
            BankAccount account = new BankAccount(customerName, accountType, openingDeposit);
            account.displayAccountDetails();
            System.out.println("You selected: " + choice);
        }
        else if (choice == 2) {
            System.out.println("Thank you for using VaultCore!");
        }
        else {
            System.out.println("Invalid choice!");
        }
    }
}