from bs4 import BeautifulSoup
import requests,time


# def scrap_stock_data():
#     session=requests.Session()

#     url='https://query1.finance.yahoo.com/v7/finance/chart/NFLX/'
#     headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'}
#     session.get("https://finance.yahoo.com", headers=headers)

#     time.sleep(5)  # mimic human delay
#     response=session.get(url,headers=headers)
#     print('status_code-->',response.headers)
#     print(response.text[:500])
#     if response.status_code==200:    
#         data=response.json()
#         print(data)
    


# scrap_stock_data()
import csv
import random

names = [
    "Amit Sharma", "Rahul Verma", "Priya Singh", "Neha Gupta", "Vikas Yadav",
    "Anjali Mehta", "Rohit Kumar", "Sneha Kapoor", "Karan Malhotra", "Pooja Tiwari",
    "Suresh Patel", "Deepak Mishra", "Kavita Joshi", "Nitin Agarwal", "Ritika Jain",
    "Arjun Kapoor", "Meena Nair", "Manoj Tiwari", "Priyanka Das", "Ajay Singh"
]

designations = [
    "Software Engineer", "Data Analyst", "HR Manager", "Accountant",
    "Project Manager", "Sales Executive", "Marketing Manager",
    "Business Analyst", "Support Engineer", "DevOps Engineer"
]

with open("employees.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["emp_id", "name", "designation"])

    for i in range(1, 501):
        emp_id = 1000 + i
        name = random.choice(names)
        designation = random.choice(designations)
        writer.writerow([emp_id, name, designation])

print("employees.csv created successfully")