import csv
from math import sqrt

data_file = './data/sampleData.csv'


def load_csv(file_name):   
    ids = []
    names = []
    hours = []
    grades = []

    with open(file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            ids.append(int(row['id']))
            names.append(row['name'])
            hours.append(float(row['hours']))
            grades.append(float(row['score']))
            
    return {"ID":ids, "Name": names, 
            "Hours": hours, "Grade": grades}



def display_data(**kwargs):
    columns = kwargs.keys()
    values = kwargs.values()
    dataset = list(zip(*values))
    
    indent = f'{"":5}'
    
    def spacer(index, val):
        if index == 1:
            return f'{val:<20}' 
        else:
            return f'{val:<10}'
        
    # columns_names = list( map(lambda index, x: spacer(index, x), enumerate(columns)) )
    columns_names = [spacer(index, val) for index, val in enumerate(columns)]
    table_header = indent + ''.join(columns_names)
    
    dashed_line_length = len(table_header)

    border_dashes = '-' * dashed_line_length 
    print(border_dashes)
    print(table_header)
    print(border_dashes)
    for i in range(len(dataset)):
        row_i_spaced = [spacer(index, val) for index , val in enumerate(dataset[i])]
        row_i = indent + ''.join(row_i_spaced)
        print(row_i)
    print(border_dashes)
    
    
def grade_to_alphapet(grade_numeric):
    if 90 <= grade_numeric <= 100:
        return 'A'
    elif grade_numeric >= 75:
        return 'B'
    elif grade_numeric >= 60:
        return 'C'
    elif grade_numeric >=50:
        return 'D'
    else: 
        return 'F'
    
    
def compute_grades(dataset):
    dataset_copy = dataset.copy()
    dataset_copy.pop('Hours', None)
    dataset_copy['Grade'] = list( map(grade_to_alphapet, dataset_copy['Grade']) )
    display_data(**dataset_copy)


def search_by_name(dataset, name):
    names_list = map(lambda x: x.lower() ,dataset['Name'])
    found_indices = [index for index, full_name in enumerate(names_list) if name in full_name]
    
    search_result_dict = {}
    
    for key in dataset:
        search_result_dict[key] = [dataset[key][i] for i in found_indices]
        
    display_data(**search_result_dict)


def mean(arr):
    return sum(arr) / len(arr)

# var(x) = 1/n-1 sum((x-x_bar)**2)
def var(arr):
    arr_mean = mean(arr)
    diff = [(el-arr_mean)**2 for el in arr]
    variance = sum(diff) / (len(diff) - 1)
    return round( variance, 2 )


def std(arr):
    return round(sqrt(var(arr)), 2)


def calculate_descriptive_statistics(dataset):
    
    hours = dataset['Hours']
    grades = dataset['Grade']
    
    stats =  {
        '----': ['Hours', 'Score'],
        'Mean': [mean(hours), mean(grades)],
        'Variance': [var(hours), var(grades)],
        'Standard Deviation': [std(hours), std(grades)]
    }
    
    display_data(**stats)
    

# b1 = (sum(xy) - x_bar * y_bar) / (sum(x**2) -n*x_bar**2)
def calculate_regression_param(dataset, independent, dependent):
    x = dataset[independent]
    y = dataset[dependent]
    n = len(x)
    
    xy = [ x[i]*y[i] for i in range(n) ]
    x_square = [_x**2 for _x in x] 
    
    b1 = ( sum(xy) - n*mean(x)*mean(y) ) / ( sum(x_square) - n*mean(x)**2 )
    b0 = mean(y) - b1*mean(x)
    
    return b0, b1

# y = b0 + b1*x
def predict_grade(dataset, hours):
    b0, b1 = calculate_regression_param(dataset, 'Hours', 'Grade')
    
    return b0 + b1*hours
    

dataset = load_csv(data_file)
# display_data(**dataset)
# compute_grades(dataset)
# calculate_descriptive_statistics(dataset)
# search_name = input('Please enter the name you are looking for: ')
# search_by_name(dataset, search_name)
# display_reg_equation(dataset)
# predict_g(dataset)


if __name__ == '__main__':
    dataset = {
               "ID":[],
               "Name": [], 
               "Hours": [], 
               "Grade": []
               }
    
    def load_data():
        global dataset
        dataset = load_csv(data_file)
        # print(dataset)
    
    def list_data():
        display_data(**dataset)
        
    def compute_show_grades():
        compute_grades(dataset)
        
    def search_name():
        name = input('Enter the name you want to look for: ')
        search_by_name(dataset, name)
        
    def descriptive_Stats():
        calculate_descriptive_statistics(dataset)
        
    def format_output(output):
        border_dashes = '-' * 60
        print(border_dashes)
        print(output.center(60))
        print(border_dashes)

    def display_reg_equation(dataset):
        b0, b1 = calculate_regression_param(dataset, 'Hours', 'Grade')
        reg_equation_str = f'Score = {round(b0, 3)} + {round(b1, 3)} * Hours'
        format_output(reg_equation_str)

        
    def display_predict_grade(dataset):
        study_hours = float(input('Enter the number of study hours: '))
        predicted = round(predict_grade(dataset, study_hours), 3)
        prediction_str = f'Predicted score = {predicted}'
        format_output(prediction_str)
            
    def reg_analysis():
        display_reg_equation(dataset)
        
    def predict_score():
        display_predict_grade(dataset)
        
    def exit_system():
        global run
        print('See you soon!')
        run = False
        
    operations = {
        "1": {"func": load_data, "title": "Read Data"},
        "2": {"func": list_data, "title": "List Data"},
        "3": {"func": compute_show_grades, "title": "Compute and Show Grades"},
        "4": {"func": search_by_name, "title": "Search by Name"},
        "5": {"func": descriptive_Stats, "title": "Descriptive Statistics"},
        "6": {"func": reg_analysis, "title": "Regression Analysis"},
        "7": {"func": predict_score, "title": "Prediction"},
        "9": {"func": exit_system, "title": "Exit the System"}
    }
    
    run = True
    

    def execute_operation(operations, operation_index, dataset):
        operation_name = operations[operation_index]["title"]
        operation_func = operations[operation_index]["func"]
        
        if not run: return

        if operation_index in operations.keys():
            if int(operation_index) == 1:
                print(f'{operation_index}- {operation_name}...')
                operation_func()
            if int(operation_index) in range(2,8):
                print(f'{operation_index}- {operation_name}...')
                operation_func()
            if int(operation_index) == 9:
                operation_func()
                return
            print(f'{operation_name} has finished successfully.\n')
            get_user_option(dataset, operations)
        else:
            print("\nThe option you chose is not in the list, please choose a valid option from the list below!\n")
            options_prompt(operations)
            get_user_option(dataset, operations)
    

    
    def options_prompt(operations):
        for index, operation in operations.items():
            print(f'{index}- {operation["title"]}')

    def get_user_option(dataset, operations):
        user_option = input('Please choose an option (enter the option number): ')
        execute_operation(operations, user_option, dataset)
    
    
    welcome_msg = ['Welcome to GRADES_STATS V1.0', 'Designed By Alaa Mirghani']
    welcome_msg_str = '\n'.join([line.center(60) for line in welcome_msg])
    format_output(welcome_msg_str)
    print(" ")
    options_prompt(operations)
    print(" ")
    get_user_option(dataset, operations)
    
