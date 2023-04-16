# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:36:34 2023

@author: IAmYodea
"""

# Write a function that does preliminary cleaning i.e. converts input to string; lower_boundcases it; removes all punctuations and currency symbols

def remove_punctuations_and_symbols(sal_string: str, curr_symbols: str = "", keep_punct: str = "") -> str:
    '''
    This function does preliminary cleaning of a salary string:
    1. Converts the input to a string.
    2. Converts the input to lowercase.
    3. Removes all currency symbols specified in the curr_symbols parameter and
       all punctuation characters except for those specified in the keep_punct parameter.

    Args:
        sal_string (str): The input string to clean.
        curr_symbols (str): A string containing all currency symbols to remove from the text. Default is an empty string.
        keep_punct (str): A string containing all punctuation characters to keep in the text. Default is an empty string.

    Returns:
        A cleaned version of the input string, with all currency symbols and unnecessary punctuation removed.
    '''
    # Convert the input to a string (if it's not already a string).
    sal_string = str(sal_string)

    # Convert the input to lowercase.
    sal_string = sal_string.lower()

    # Define the characters to remove.
    remove_chars = curr_symbols + ''.join([char for char in string.punctuation if char not in keep_punct])

    # Remove the characters from the text.
    sal_string = sal_string.translate(str.maketrans('', '', remove_chars))

    # Return the cleaned text.
    return sal_string


# Write a function to extract salaries from string, be they single salaries or salary ranges

def extract_possible_salaries(sal_string: str):
    '''
    This function extracts possible salaries from a given string. It looks for
    any number with an optional decimal point, followed by an optional 'k' or 'm'
    to represent thousands or millions, respectively.

    Args:
      sal_string (str): The input string to search for possible salaries.

    Returns:
      If the input string contains a single salary, returns the salary as a string.
      If the input string contains a salary range, returns a list of salaries as strings.
      If the input string does not contain any salaries, returns an empty list.
    '''

    # Compile the regex pattern for faster matching.
    pattern = re.compile(r'\d+[.]*\d*[km]*\d*[.]*\d*[km]*')

    # Find all matches for the salary pattern in the string.
    matches = [match.group(0) for match in pattern.finditer(sal_string)]

    # Return the single salary as a string if only one match was found.
    # Otherwise, return the list of salaries as strings.
    return matches[0] if len(matches) == 1 else matches

# Write  a function to convert 'k' to '000' and 'm' to '000000'
def convert_salary_to_numeric(sal_string, k_or_m=''):  
    """
    This function converts a salary string to a numeric value.

    Parameters:
    sal_string (str): The salary in string format.

    k_or_m (str, optional): The unit of measurement for the salary, either "k" or "m". 
        Defaults to an empty string.

    Returns:
    float: The numeric representation of the salary.
    """
    
    # Check if the input salary is already a numeric value
    if isinstance(sal_string, int) or isinstance(sal_string, float):
        # If yes, simply return the numeric value
        return float(sal_string)

    # Check if the input salary is a string
    elif isinstance(sal_string, str):
        # Check if the unit of measurement is either 'k' or 'k' is present in the salary string
        if (k_or_m == 'k') or ('k' in sal_string):
            # If yes, remove the 'k' from the salary string and convert it to a numeric value
            return float(sal_string.strip().strip("k").replace("000", '')) * 1000
        
        # Check if the unit of measurement is either 'm' or 'm' is present in the salary string
        elif (k_or_m == 'm') or ('m' in sal_string):
            # If yes, remove the 'm' from the salary string and convert it to a numeric value
            return float(sal_string.strip().strip("m").replace("000000", '')) * 1000000
        
        # If the unit of measurement is not specified or present in the salary string
        else:
            # Convert the salary string to a numeric value
            return float(sal_string.strip())
    # If the input salary is not a string or a numeric value
    else:
        # Attempt to convert the salary to a numeric value
        # return float(sal_string.strip())
        try:
            return float(sal_string.strip())
        except ValueError:
            return None

def process_salary_ranges(sal_range):
    """
    This function processes a list of salary ranges and returns a list of [lower_bound, upper_bound].
    It handles salary ranges in k, m, or just numbers.

    Parameters:
    sal_range (list): The list of salary ranges.

    Returns:
    list: A list of [lower_bound, upper_bound].
    """
    # First, drop any number that's equal to one of the last 100 years
    sal_range = [n for n in sal_range \
                 if ('k' in n) \
                or ('m' in n) \
                or not (datetime.datetime.now().year - 100) <= convert_salary_to_numeric(n) <= (datetime.datetime.now().year)]

    # If all the numbers were equal to one of the last hundred years, this means the salary is between the current year and 100 years ago.
    if len(sal_range) == 0: # If all numbers were equal to one of the last hundred years, they were dropped, hence the list will be empty. 
      sal_range = [datetime.datetime.now().year - 100, datetime.datetime.now().year]
      return sal_range
    
    # If only one value is left, run convert_salary_to_numeric on it and return the result
    elif len(sal_range) == 1:
      return [convert_salary_to_numeric(sal_range[0])]

    # Now let's actually deal with the ranges
    else: 
          # Let's handle scenarios where there are two numbers but it isn't a range. In a range, the second number will be greater than the first
          if convert_salary_to_numeric(sal_range[1]) < convert_salary_to_numeric(sal_range[0]):
            return [convert_salary_to_numeric(sal_range[0])]
          
          # Let's handle salary ranges in thousands. Focus on sal_range[1] because the larger number is usually mentioned last in a range 
          # When 'k' is in the second value
          elif 'k' in sal_range[1]:
            upper_bound = convert_salary_to_numeric(sal_range[1])

            # If the first value has 'k'
            if 'k' in sal_range[0]:
              lower_bound = convert_salary_to_numeric(sal_range[0])

            # If the first value doesn't have 'k' in it
            else:
              # For scenarios like '10 - 50k', if 10 * 1000 is less than 50000, then multiply 10 by 1000; else return 10 as is.
              if convert_salary_to_numeric(sal_range[0], 'k') < upper_bound :
                lower_bound = convert_salary_to_numeric(sal_range[0], 'k')
              
              # For scenarios like '10000 - 50k'
              else:
                lower_bound = convert_salary_to_numeric(sal_range[0])

            return [lower_bound, upper_bound]

          # When 'm' is in the second value
          elif 'm' in sal_range[1]:
            upper_bound = convert_salary_to_numeric(sal_range[1])
            
            # If the first value has 'm'
            if 'm' in sal_range[0]:
              lower_bound = convert_salary_to_numeric(sal_range[0])

            # If the first value doesn't have 'm' in it
            else:
              # For scenarios like '5 - 1000000'
              if convert_salary_to_numeric(sal_range[0], 'm') < upper_bound :
                lower_bound = convert_salary_to_numeric(sal_range[0], 'm')
              
              # For scenarios like '1000000 - 50m'
              else:
                lower_bound = convert_salary_to_numeric(sal_range[0])
            
            return [lower_bound, upper_bound]
    
          # For scenarios where the second value doesn't contain 'k' or 'm' AND is less than 1,000,000
          elif convert_salary_to_numeric(sal_range[1]) < 1000000:
            upper_bound = convert_salary_to_numeric(sal_range[1])

            # If the first value has 'k' in it e.g. '5k - 50000'
            if 'k' in sal_range[0]:
              lower_bound = convert_salary_to_numeric(sal_range[0])
            # If the first value doesn't have 'k' in it e.g. 5000 - 50000
            else:
              # For scenarios like '10 - 50000'
              if convert_salary_to_numeric(sal_range[0], 'k') < upper_bound :
                lower_bound = convert_salary_to_numeric(sal_range[0], 'k')
              
              # For scenarios like '10000 - 50k'
              else:
                lower_bound = convert_salary_to_numeric(sal_range[0])

            return [lower_bound, upper_bound]
          
          # For scenarios where the second value doesn't contain 'k' or 'm' AND is >= 1,000,000
          elif convert_salary_to_numeric(sal_range[1]) >= 1000000:
            
            upper_bound = convert_salary_to_numeric(sal_range[1])

            # For scenarios like '3 - 5,000,000'
            if convert_salary_to_numeric(sal_range[0], 'm') < upper_bound :
              lower_bound = convert_salary_to_numeric(sal_range[0], 'm')
            
            # For scenarios like '3,000,000 - 5,000,000'
            else:
              lower_bound = convert_salary_to_numeric(sal_range[0])
            
            return [lower_bound, upper_bound]

          # What to do in other cases
          else:
            return [convert_salary_to_numeric(n) for n in sal_range]

def avg_salary_ranges(sal_range):
    """
    This function calculates the average of salary ranges in the format of string or a list of values.
    It can handle salary ranges in k, m or just numbers. If sal_range has only one
    value, it returns that value.

    Parameters:
    sal_range (str): The salary range in string or list format.

    Returns:
    float: The average of the salary range or the salary value if the range has only one value.
    """
    # If input is an empty list, an empty string, or None.
    if not sal_range:
        return "Not provided"

    # If input is not a list
    elif not isinstance(sal_range, list):
        try:
          return convert_salary_to_numeric(sal_range)
        except:
          return "Can't convert to numeric"
    
    # If input is a list that isn't empty    
    else:
      salary_numbers = process_salary_ranges(sal_range)
      
      # If there is only one value after processing
      if len(salary_numbers) == 1:
          return salary_numbers[0]

      # Now let's actually deal with the ranges
      else:
          salary_numbers = sorted(salary_numbers)

          # Calculate the mean of the salary range and return that
          try:
            return statistics.mean(salary_numbers)
          except:
            return "statistics.mean failed to run"

# A function that takes a string as input and replaces occurrencies of 'dollar', 'euro', 'pound', 'yen' with their corresponding symbols

def replace_currency_words_with_symbols(string):
    '''
    This function takes a string as input and replaces occurrences of 'dollar',
    'euro', 'pound', and 'yen' with their corresponding currency symbols.

    Args:
        string (str): The string to search for currency words.

    Returns:
        A new string with any currency words replaced by their corresponding symbols.
    '''
    
    # Define a dictionary with currency words as keys and currency symbols as values.
    symbols_map = {
        "dollar": "$",
        "euro": "€",
        "pound": "£",
        "yen": "¥"
    }
    
    # Create a regular expression pattern to match any of the keys in the symbols_map dictionary.
    # Use re.escape to escape any special characters in the keys.
    pattern = '|'.join(map(re.escape, symbols_map.keys()))

    # Use re.sub to replace any occurrences of the pattern in the input string with the corresponding currency symbol.
    # The lambda function inside re.sub gets the matched object as input and returns the corresponding value from the symbols_map dictionary.
    return re.sub(pattern, lambda x: symbols_map[x.group()], string)

# Define function to convert (pound, euro, and japanese yen) to dollar

def convert_to_dollar(source_string, salary):
    """
    Convert salary from pound, euro, or japanese yen to dollar using exchange rates from the kraken exchange.

    Args:
    source_string (str): A string containing the currency symbol of the original salary, e.g. "$100", "£100", "€100", or "¥100".
    salary (float): The original salary as a float.

    Returns:
    float: The converted salary in dollars.
    """
    
    exchange = ccxt.kraken()

    # First, let's replace occurrencies of 'dollar', 'euro', 'pound', 'yen' in the source_string with their corresponding symbols 
    source_string = replace_currency_words_with_symbols(source_string)

    # Now, let's look for the currency symbols in the string   
    curr = re.search(r'[$£€¥]', source_string)

    if curr is None:    # If there are no currency signs, assume it's already in dollars and return salary
      return salary
    
    else:
      curr = curr.group(0)
      
      if curr == '$':   # If the currency sign is dollars, return salary
        return salary

      elif curr == '£':
        ticker = exchange.fetch_ticker("GBP/USD")
        rate = ticker['last']
  
        return round(salary * float(rate))
        
      elif curr == '€':
        ticker = exchange.fetch_ticker("EUR/USD")
        rate = ticker['last']
  
        return round(salary * float(rate))

      elif curr == '¥':
        ticker = exchange.fetch_ticker("USD/JPY")
        rate = ticker['last']
  
        return round(salary / float(rate))
      
      else:
        return salary

# Define function to convert annual salaries to monthly salaries

def annual_to_monthly(source_string, salary):
    """
    Convert an annual salary to a monthly salary if the source string suggests that
    the salary is annual. If the salary is already in monthly terms or the source
    string doesn't suggest that the salary is annual, return the input salary.

    Args:
    - source_string (str): A string that provides context about the salary amount
    - salary (float): A salary amount in dollars

    Returns:
    - float: The input salary converted to monthly terms, if it appears to be annual
    """
    # Create a list of the last 100 years, and check if any are mentioned in the source string
    recent_years = list(reversed(range(datetime.datetime.now().year - 100, datetime.datetime.now().year + 1)))
    recent_years_str = [str(recent_year) for recent_year in recent_years]
    pattern = r'\b({})\b'.format('|'.join(recent_years_str))

    # If the string contains 'annual', '/y', or 'year', or it mentions a year in the last 100 years, or
    # it contains at least three numeric values that might be salaries (after replacing commas with nothing),
    # we assume it is an annual salary and divide it by 12 to convert to monthly terms.
    if (re.search(r'annual|\/y|year', source_string)) or \
            (re.search(r'(in|on)\s*(\d{4})', source_string, re.IGNORECASE)) or \
            (len(re.findall(r'\d+[.]*\d*[km]*\d*[.]*\d*[km]*', source_string.replace(',', ''))) >= 3):
        return salary / 12
    else:
        return salary

# Define the final function that will clean a string and extract salary from it
def extract_salary(sal_string, convert_to_monthly = False):
  """
    Extract salary from an unclean, unstructured string

    Args:
    sal_string (str): The string containing the salary

    Returns:
    int: The converted salary in dollars.
    str: 'Not provided' if the string doesn't contain salaries
  """
  
  if isinstance(sal_string, int) or isinstance(sal_string, float):  # If it's already float or int, return it as float
    return float(sal_string)
  
  else: 
    # First, remove punctuations and currency symbols from the string
    prelim_string = remove_punctuations_and_symbols(sal_string, curr_symbols="$£€¥", keep_punct="-./")

    # Extract possible salaries from the prelim_string
    extracted_sal = extract_possible_salaries(prelim_string)

    # Clean up the salaries in extracted_sal, dropping numbers that aren't salaries, changing k to 1000 and m to 1000000, etc.
    clean_salary = avg_salary_ranges(extracted_sal)

    # Convert salaries reported in currencies other than US dollar to USD
    correct_denom = convert_to_dollar(sal_string, clean_salary)

    # Convert salaries reported as annual to monthly
    if convert_to_monthly == True:
        final_salary = annual_to_monthly(sal_string, correct_denom)
    
    # Just in case final_salary is still a string, return as is; Otherwise, convert to int and return.
    if isinstance (final_salary, str):
      return final_salary
    else:
      return int(round(final_salary))