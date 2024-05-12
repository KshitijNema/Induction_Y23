#include<iostream>
#include<string>
#include<vector>
#include<cstdlib>
#include<ctime>
using namespace std;


class statement{
    private:
    time_t date;
    double amount;

    public:
    statement(double amount) : date(time(nullptr)), amount(amount) {}
    void print() const {
        cout << "Date: " << asctime(localtime(&date)) << "Amount: " << amount << endl;
    }
};


class Account{
    private:
    int accnumber;
    double balance;
    time_t opendate;
    string type;
    vector<statement> statements;


    public:
    Account(int accnumber, double initialbalance, string acctype): accnumber(accnumber), balance(initialbalance), type(acctype), opendate(time(nullptr)) {}

    int getaccnumber() const{
        return accnumber;
    };
    void addtransaction(double amount) {
        balance = balance + amount;
        statements.push_back(statement(amount));
    }


};


class accholder{
    private:
    string name;
    string username;
    string password;
    vector<Account> accounts;

    public:
    accholder(string usernamea, string p) : username(usernamea), password(p) {}
    void createacc(double initialbalance, string type) {
        int accnumber = rand() % 900000000 + 100000000;
        accounts.push_back(Account(accnumber, initialbalance, type));
    }
    void changepassword(string newpassword){
        password= newpassword;
    }
    void viewstatements() const {
        for (const auto& account : accounts) {
            cout << "Account Number: " << account.getaccnumber() << endl;
        }
    }
    

};

class BranchManager {
public:
    void fastForward(int days) {
        cout << "Time fast forwarded by " << days << " days.\n";
    }
};

class CLI {
public:
    void run() {
        string username, password;
        cout << "Greetings from World Bank!!!!\n";
        cout << "Enter username: ";
        cin >> username;
        cout << "Enter password: ";
        cin >> password;

        if (username == "manager" && password == "manager") {
            BranchManager manager;
            int days;
            cout << "Logged in.\n";
            cout << "Number of days to fast forward: ";
            cin >> days;
            manager.fastForward(days);
            return;
        }

        accholder user(username, password);

        int choice;
        do {
            cout << "\nMenu:\n";
            cout << "1. Create Account\n";
            cout << "2. View Statements\n";
            cout << "3. Exit\n";
            cout << "What do you want to do: ";
            cin >> choice;

            if (choice==1){
                    string type;
                    double initialBalance;
                    cout << "Enter account type (savings/checking): ";
                    cin >> type;
                    cout << "Enter initial balance: ";
                    cin >> initialBalance;
                    user.createacc(initialBalance, type);
                    cout << "Account created successfully!\n";
                    break;
                }
                else if(choice==2) {
                    user.viewstatements();
                    break;
                }
                else if(choice==3) {
                    cout << "Exitted\n";
                    break;
                }
                else {
                    cout << "Please choose a valid integer between 1-3\n";
                }
            }
        while (choice != 3);
    };
};

int main() {
    srand(time(nullptr));
    CLI cli;
    cli.run();

    return 0;
}






