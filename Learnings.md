Yes, the function can be simplified while retaining its functionality. Here's a more concise version of your `get_requirements` function:

```python
import os
from typing import List

def get_requirements() -> List[str]:
    '''
    Reads requirements.txt and returns a list of requirements to be installed.
    '''
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
    try:
        with open(requirements_path, 'r') as file:
            return [line.strip() for line in file if line.strip() and line.strip() != '-e .']
    except FileNotFoundError:
        print('Requirements file not found.')
        return []
```

### Simplifications:
1. **One-Line List Comprehension**:
   - Combines the reading, stripping, filtering, and appending into a single list comprehension: `[line.strip() for line in file if line.strip() and line.strip() != '-e .']`.

2. **Dynamic File Path**:
   - Ensures the function works regardless of where it's called by dynamically determining the absolute path to `requirements.txt`.

3. **Return Statement**:
   - Directly returns the list of requirements instead of using an intermediate list (`requirement_lst`).

4. **Error Handling**:
   - Keeps `FileNotFoundError` handling for missing files but simplifies the `print` statement and ensures an empty list is returned.

### Usage Example:
- Place this function in your `setup.py` file.
- Ensure `requirements.txt` is in the same directory.
- Call the function and check:
   ```python
   print(get_requirements())  # Outputs the list of requirements
   ```

This version is not only concise but also clear and easy to understand, making it ideal for simple use cases. 

The use of `if __name__ == "__main__":` in Python determines whether a script is being run directly or being imported as a module. However, in your case, whether you include it or not, you are running `python setup.py`, which executes the script in the same way each time, so you see the same result.

### **Understanding `if __name__ == "__main__":`**
- Every Python script has a built-in variable called `__name__`.
- When a script runs directly (e.g., `python setup.py`), `__name__` is set to `"__main__"`, so the code inside `if __name__ == "__main__":` executes.
- If the script is imported as a module into another script, `__name__` is set to the script's filename (not `"__main__"`), and the code inside this block does **not** execute automatically.

### **When Does It Make a Difference?**
If you import your script in another Python file, the behavior will change.

#### **Example Without `if __name__ == "__main__":`**
**File: `setup.py`**
```python
from typing import List

def get_requirements() -> List[str]:
    """Reads requirements.txt and returns a list of dependencies."""
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('Requirements file not found.')
    
    return requirement_lst

print(get_requirements())  # This runs every time the file is imported
```

**File: `test.py`**
```python
import setup  # Importing setup.py
```
#### **Output when running `python test.py`:**
```
['requirement1', 'requirement2', ...]  # (This prints automatically when test.py is run)
```
- Here, `print(get_requirements())` is executed **immediately** when `setup.py` is imported, which is often **not desired**.

---

#### **Example With `if __name__ == "__main__":`**
**Modified `setup.py`**
```python
from typing import List

def get_requirements() -> List[str]:
    """Reads requirements.txt and returns a list of dependencies."""
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('Requirements file not found.')
    
    return requirement_lst

if __name__ == "__main__":
    print(get_requirements())  # This runs ONLY when executed directly
```

**File: `test.py`**
```python
import setup  # Importing setup.py
```

#### **Output when running `python test.py`:**
```
(Nothing prints because `print(get_requirements())` is inside `if __name__ == "__main__":`)
```

- **Now, `setup.py` does not execute `print(get_requirements())` when imported into another script.** 
- This is useful when writing reusable modules.

### **Summary**
- If you run `python setup.py` directly, it behaves the same with or without `if __name__ == "__main__":` because Python executes the file.
- If you **import** the script into another file, the code inside `if __name__ == "__main__":` does **not** execute, preventing unintended behavior.

Let me know if you need further clarification! 🚀

Great question! Let’s break it down and explore how `setup.py` and `requirements.txt` interact and the purpose of the `-e .` flag.

---

### **How `setup.py` and `requirements.txt` Are Connected**

1. **Purpose of `setup.py`**:
   - `setup.py` is a Python script used to package and distribute your Python project. It provides metadata (name, version, dependencies, etc.) about your project and enables tools like `pip` or `setuptools` to install it.
   - It specifies dependencies that your package requires through the `install_requires` parameter in the `setup()` function. For example:
     ```python
     setup(
         name='MyProject',
         version='1.0',
         install_requires=[
             'numpy',
             'pandas',
             'scikit-learn'
         ]
     )
     ```

2. **Purpose of `requirements.txt`**:
   - `requirements.txt` is typically used to list all dependencies (packages and their versions) for a project. When you run:
     ```sh
     pip install -r requirements.txt
     ```
     Pip installs all the packages listed in the file into the environment.

3. **How They Interact**:
   - If `requirements.txt` contains `-e .` (editable mode), it tells `pip` to look at the `setup.py` file in the current directory (`.`) to install the project. This effectively connects `requirements.txt` with `setup.py`.
   - When `pip` encounters `-e .`, it installs the package as an editable package and uses the metadata and dependency information from `setup.py` to resolve dependencies.

---

### **What Does `-e .` Do?**

1. **Editable Mode**:
   - The `-e .` flag means "install this package in editable mode."
   - In editable mode, the project files remain in their original location (rather than being copied to a site-packages directory). Any changes you make to the source files are immediately reflected without reinstalling the package.

2. **Why Is It Useful?**
   - It’s particularly useful during development, as it allows you to work on your project and test it without reinstalling the package every time you make changes.
   - For example:
     - If you’re writing a library or package, you can keep modifying the code and still use it as if it’s installed without re-running `pip install`.

3. **How `setup.py` Works with `-e .`**:
   - When you run `pip install -r requirements.txt` and `-e .` is listed, Pip looks at the `setup.py` file in the current directory (`.`) and processes the project as a package.
   - Dependencies listed in `install_requires` in `setup.py` are automatically installed.

---

### **Example**

#### File: `setup.py`
```python
from setuptools import setup, find_packages

setup(
    name="example_package",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy==1.21.0",
        "pandas>=1.3.0"
    ]
)
```

#### File: `requirements.txt`
```
-e .
requests==2.25.1
```

#### Command:
```sh
pip install -r requirements.txt
```

#### What Happens:
1. Pip sees `-e .` in `requirements.txt`:
   - It processes `setup.py` to install the project `example_package` in editable mode.
   - It installs the dependencies listed in `install_requires` of `setup.py` (i.e., `numpy` and `pandas`).
2. Pip also installs the additional dependency specified in `requirements.txt` (i.e., `requests`).

---

### **Key Points to Remember**
- `setup.py` is for packaging and distributing your project, and `install_requires` specifies dependencies.
- `requirements.txt` is for explicitly listing dependencies for installation.
- The `-e .` flag in `requirements.txt` ties it to `setup.py`, enabling editable installation.

Certainly! Here's a brief overview of both:

1. **PyMongo**:
   - **Use**: PyMongo is a Python library used to interact with MongoDB, a NoSQL database. It allows developers to connect to MongoDB, perform operations like inserting, updating, querying, and deleting data, and manage databases and collections programmatically.
   - **Key Features**: Provides an easy-to-use API for MongoDB commands, supports advanced features like aggregation pipelines, and handles data encoding/decoding between Python and MongoDB formats.

2. **Certifi**:
   - **Use**: Certifi is a Python package that provides a curated collection of trusted root certificates for SSL/TLS verification. It ensures secure HTTPS connections when accessing remote servers or databases.
   - **Importance with PyMongo**: When connecting to a MongoDB instance (especially on the cloud, like MongoDB Atlas), certifi helps verify the server’s SSL certificate, ensuring a secure connection.

In summary, PyMongo is for database operations, while certifi ensures secure, trusted communication between your application and the database. 

The `__pycache__` directory is automatically created by Python when you run a script. Here's a brief explanation:

### **How `__pycache__` is Created**
- When you execute a Python program, Python compiles the `.py` (source code) files into bytecode to make execution faster.
- These compiled bytecode files are stored in the `__pycache__` directory with a `.pyc` extension (e.g., `module_name.cpython-311.pyc`).
- Python does this to avoid recompiling the source code every time the program runs, provided the source code has not changed.

### **What Is Its Use?**
1. **Performance Optimization**:
   - The bytecode stored in `__pycache__` helps speed up the execution of Python programs.
   - When you rerun the program, Python checks the timestamp of the source code. If it hasn’t changed, it uses the cached bytecode instead of recompiling the `.py` file.

2. **Cross-Compatibility**:
   - The `.pyc` files in `__pycache__` are optimized for the Python interpreter version used to run the code (hence the naming like `cpython-311.pyc` for Python 3.11).
   - This ensures compatibility between different versions of Python.

3. **Reusable Bytecode**:
   - If you import modules or packages, the compiled bytecode in `__pycache__` is used to execute them quickly, rather than reinterpreting the source code each time.

### **Is `__pycache__` Required?**
- While not critical, it significantly improves performance. If you delete the `__pycache__` folder, Python will simply regenerate it the next time the program runs.

### **When to Ignore It**
- For version control systems like Git, you typically add `__pycache__/` to `.gitignore` to avoid committing these auto-generated files, as they are environment-specific.

So, in short, `__pycache__` is a behind-the-scenes optimization that helps Python run your code more efficiently! 

A `.env` file is used to store environment variables in a project. These variables can include sensitive information such as API keys, database credentials, or configuration details. The purpose of using a `.env` file is to separate sensitive data and configuration settings from the main codebase, improving security and flexibility.

### **Key Uses of `.env`**:
1. **Security**:
   - Keeps sensitive credentials out of the source code, which prevents accidental exposure (e.g., on GitHub).
   
2. **Configuration Management**:
   - Makes it easier to manage environment-specific settings (e.g., development, staging, production) by using different `.env` files for different environments.

3. **Ease of Use**:
   - Developers can load the variables into their application using libraries like `python-decouple` or `dotenv` in Python.

### Example `.env` File:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
API_KEY=your_api_key_here
DEBUG=True
```

These variables can then be accessed programmatically, avoiding hardcoding them into your codebase. 

The two code snippets you provided achieve similar outcomes (converting a DataFrame to a list of records) but use different methods. Here's a breakdown of the differences:

### **1. `data.to_dict(orient='records')`**:
- **Method**: Uses the `to_dict` method with the `orient='records'` argument.
- **Outcome**: Converts the DataFrame into a list of dictionaries, where each dictionary represents a row in the DataFrame.
- **Efficiency**: Generally more efficient and straightforward for converting DataFrames to a list of records.
- **Example**:
  ```python
  return data.to_dict(orient='records')
  ```
  ```json
  [
    {"column1": "value1", "column2": "value2"},
    {"column1": "value3", "column2": "value4"}
  ]
  ```

### **2. `json.loads(data.T.to_json()).values()`**:
- **Method**: First transposes the DataFrame (`data.T`), converts it to JSON, then parses the JSON string back into a Python dictionary and extracts the values.
- **Outcome**: Produces a list of dictionaries, similar to the first method, but involves extra steps and more transformations.
- **Complexity**: More complex due to the additional JSON serialization and deserialization steps.
- **Example**:
  ```python
  records = json.loads(data.T.to_json()).values()
  return list(records)
  ```
  ```json
  [
    {"column1": "value1", "column2": "value2"},
    {"column1": "value3", "column2": "value4"}
  ]
  ```

### **Comparison**:
- **Performance**: `to_dict(orient='records')` is generally faster and less resource-intensive since it directly converts the DataFrame to the desired format without additional intermediate steps.
- **Readability**: `to_dict(orient='records')` is more readable and easier to understand, which is beneficial for code maintenance and collaboration.

### **Recommendation**:
- **Use `to_dict(orient='records')`**: It’s simpler, more efficient, and more readable for converting a DataFrame to a list of dictionaries.

### Purpose of the Code in `__init__.py`

The code in your `__init__.py` file defines a set of constants that are used throughout your machine learning pipeline for network security. Constants are values that do not change during the execution of the program and are typically used to improve code readability and maintainability. Here’s a detailed explanation of the code:

### **Defined Constants and Their Uses**

1. **General Constants**:
   ```python
   TARGET_COLUMN = "Result"
   PIPELINE_NAME: str = "NetworkSecurity"
   ARTIFACT_DIR: str = "Artifacts"
   FILE_NAME: str = "phisingData.csv"
   TRAIN_FILE_NAME: str = "train.csv"
   TEST_FILE_NAME: str = "test.csv"
   ```
   - **TARGET_COLUMN**: Specifies the column in your dataset that contains the target variable (the variable you want to predict).
   - **PIPELINE_NAME**: The name of your machine learning pipeline.
   - **ARTIFACT_DIR**: Directory where artifacts (intermediate files, models, etc.) will be stored.
   - **FILE_NAME**: The name of the main CSV file containing your data.
   - **TRAIN_FILE_NAME** and **TEST_FILE_NAME**: File names for the training and testing datasets.

2. **Data Ingestion Constants**:
   ```python
   DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
   DATA_INGESTION_DATABASE_NAME: str = "SaifiAI"
   DATA_INGESTION_DIR_NAME: str = "data_ingestion"
   DATA_INGESTION_FEATURE_STORE_NAME: str = "feature_store"
   DATA_INGESTION_INGESTED_DIR: str = "ingested"
   DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
   ```
   - **DATA_INGESTION_COLLECTION_NAME**: The name of the MongoDB collection where your network data will be stored.
   - **DATA_INGESTION_DATABASE_NAME**: The name of the MongoDB database.
   - **DATA_INGESTION_DIR_NAME**: Directory for data ingestion-related files.
   - **DATA_INGESTION_FEATURE_STORE_NAME**: Directory or collection name for storing feature-engineered data.
   - **DATA_INGESTION_INGESTED_DIR**: Directory for storing ingested data.
   - **DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO**: The ratio used to split your data into training and testing sets.

### **Why Use Constants?**
- **Maintainability**: Constants make your code easier to maintain and modify. Instead of changing a value in multiple places, you can update it in one location.
- **Readability**: They make your code more readable and understandable by providing descriptive names for important values.
- **Error Reduction**: Using constants can reduce errors by avoiding hardcoding values multiple times.

The `main.py` script orchestrates the data ingestion process for the network security project. Here is a step-by-step explanation of the workflow:

### Import Necessary Modules
- The script imports various classes and modules required for data ingestion, exception handling, and logging.

### Initialize Configuration
- `TrainingPipelineConfig` is instantiated to set up the configuration for the training pipeline, including directories and timestamps.
- `DataIngestionConfig` is instantiated using the `TrainingPipelineConfig` object to set up the configuration specific to data ingestion, such as file paths and database details.

### Create Data Ingestion Object
- An instance of the `DataIngestion` class is created using the `DataIngestionConfig` object. This object will handle the entire data ingestion process.

### Initiate Data Ingestion
- The `initiate_data_ingestion` method of the `DataIngestion` object is called to start the data ingestion process. This method performs the following steps:
   - **Export Data from MongoDB**: Fetches data from the specified MongoDB collection and converts it into a pandas DataFrame.
   - **Save Data to Feature Store**: Saves the DataFrame to a CSV file in the feature store directory.
   - **Split Data into Training and Testing Sets**: Splits the DataFrame into training and testing sets and saves them as separate CSV files.

### Log and Print Results
- The script logs the successful completion of the data ingestion process and prints the paths to the training and testing files.

### Exception Handling
- If any exception occurs during the process, it is caught and a `NetworkSecurityException` is raised with the relevant error details.


## Data Drift

Data drift occurs when the statistical properties of the input data change over time, causing machine learning models to become less accurate. This happens because the model was trained on data with specific characteristics, and when those characteristics change, the model's assumptions become invalid.

### Types of Data Drift:
1. **Feature drift**: Changes in the distribution of input features
2. **Concept drift**: Changes in the relationship between input features and the target variable
3. **Label drift**: Changes in the distribution of the target variable

## Detecting Data Drift with SciPy

SciPy provides several statistical tests that can help detect data drift:

### 1. Kolmogorov-Smirnov (K-S) Test
```python
from scipy import stats

def detect_drift_ks(reference_data, current_data, feature, threshold=0.05):
    """
    Detect drift using Kolmogorov-Smirnov test
    
    Args:
        reference_data: DataFrame containing baseline data
        current_data: DataFrame containing new data to check for drift
        feature: Column name to test
        threshold: p-value threshold for significance
        
    Returns:
        boolean: True if drift detected
    """
    statistic, p_value = stats.ks_2samp(
        reference_data[feature].dropna(), 
        current_data[feature].dropna()
    )
    
    # If p-value is less than threshold, distributions are significantly different
    drift_detected = p_value < threshold
    return drift_detected, p_value, statistic
```

### 2. Chi-Square Test (for categorical features)
```python
def detect_drift_chi2(reference_data, current_data, feature, threshold=0.05):
    """Detect drift in categorical features using Chi-Square test"""
    # Get frequency distributions
    ref_counts = reference_data[feature].value_counts(normalize=True)
    curr_counts = current_data[feature].value_counts(normalize=True)
    
    # Align categories
    all_categories = sorted(set(ref_counts.index) | set(curr_counts.index))
    
    # Convert to arrays with same categories
    ref_array = np.array([ref_counts.get(cat, 0) for cat in all_categories])
    curr_array = np.array([curr_counts.get(cat, 0) for cat in all_categories])
    
    # Perform chi-square test
    statistic, p_value = stats.chisquare(curr_array, ref_array)
    
    drift_detected = p_value < threshold
    return drift_detected, p_value, statistic
```

### 3. Jensen-Shannon Distance
```python
from scipy.spatial import distance

def detect_drift_js(reference_data, current_data, feature, threshold=0.1):
    """Detect drift using Jensen-Shannon distance"""
    # Calculate distributions (can use histograms for continuous variables)
    if reference_data[feature].dtype == 'object':
        # For categorical 
        ref_dist = reference_data[feature].value_counts(normalize=True)
        curr_dist = current_data[feature].value_counts(normalize=True)
        
        # Align categories
        all_cats = sorted(set(ref_dist.index) | set(curr_dist.index))
        ref_array = np.array([ref_dist.get(cat, 0) for cat in all_cats])
        curr_array = np.array([curr_dist.get(cat, 0) for cat in all_cats])
    else:
        # For numerical, create histograms with same bins
        hist_bins = 10
        min_val = min(reference_data[feature].min(), current_data[feature].min())
        max_val = max(reference_data[feature].max(), current_data[feature].max())
        bins = np.linspace(min_val, max_val, hist_bins+1)
        
        ref_hist, _ = np.histogram(reference_data[feature].dropna(), bins=bins, density=True)
        curr_hist, _ = np.histogram(current_data[feature].dropna(), bins=bins, density=True)
        
        ref_array = ref_hist
        curr_array = curr_hist
    
    # Calculate JS distance
    js_distance = distance.jensenshannon(ref_array, curr_array)
    
    drift_detected = js_distance > threshold
    return drift_detected, js_distance
```
You can apply these tests to each feature in your dataset to identify which features are experiencing drift, and then generate a comprehensive drift report for your data validation step.

### schema.yaml
The `schema.yaml` file defines the schema for the dataset used in the network security project. It specifies the columns, their data types, and categorizes them into numerical columns. Here is a breakdown of its purpose:

### Column Definitions:
- The `columns` section lists all the columns in the dataset along with their data types (in this case, all columns are of type `int64`).

### Numerical Columns:
- The `numerical_columns` section lists the columns that are considered numerical. This can be useful for data validation, preprocessing, and feature engineering steps where numerical columns need to be treated differently from categorical or other types of columns.

This schema file can be used to ensure that the data conforms to the expected structure and types, which is crucial for data validation and preprocessing steps in the machine learning pipeline.


Here are brief notes for setting up Docker on an EC2 instance. These commands ensure that Docker is installed and configured properly for use:

---

### **Basic Steps to Set Up Docker on an EC2 Instance**

1. **Update Package List**:
   ```bash
   sudo apt-get update -y
   ```
   - Fetches the latest package lists and updates information about available software.

2. **Upgrade Installed Packages**:
   ```bash
   sudo apt-get upgrade
   ```
   - Upgrades all installed packages to their latest versions to ensure compatibility and security.

3. **Download Docker Installation Script**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   ```
   - Fetches the official Docker installation script from Docker's repository.

4. **Run the Docker Installation Script**:
   ```bash
   sudo sh get-docker.sh
   ```
   - Executes the script to install Docker on the instance, along with its dependencies.

5. **Add Current User to the Docker Group**:
   ```bash
   sudo usermod -aG docker ubuntu
   ```
   - Adds the `ubuntu` user (default user in an EC2 instance) to the `docker` group, allowing the user to run Docker commands without `sudo`.

6. **Activate Docker Group Membership**:
   ```bash
   newgrp docker
   ```
   - Refreshes the group membership for the current session, applying the changes made in the previous step without requiring a system restart.

---

### Notes:
- **Why Use `newgrp docker`?**: It eliminates the need to log out and back in for group changes to take effect.
- **Permissions**: Adding the user to the `docker` group ensures you can use Docker commands (`docker run`, `docker build`, etc.) without needing `sudo` every time.
- **Post-Setup Check**: Verify Docker installation by running:
  ```bash
  docker --version
  ```
  Or check if Docker is working:
  ```bash
  docker run hello-world
  ```

These steps will give you a fully functional Docker setup on your EC2 instance. 

Here’s a concise and clear note summarizing the steps for setting up and using a **self-hosted GitHub Actions runner on an EC2 instance**. Save this for future reference:

---

### **Setting Up a Self-Hosted GitHub Actions Runner on EC2**

1. **Pre-requisite: Docker Setup on EC2**
   - Update and upgrade the EC2 instance:
     ```bash
     sudo apt-get update -y
     sudo apt-get upgrade
     ```
   - Download and install Docker:
     ```bash
     curl -fsSL https://get.docker.com -o get-docker.sh
     sudo sh get-docker.sh
     ```
   - Add the user `ubuntu` to the Docker group and apply the change:
     ```bash
     sudo usermod -aG docker ubuntu
     newgrp docker
     ```

---

2. **Go to GitHub Repository**:
   - Navigate to **Settings** > **Actions** > **Runners**.
   - Click **Create New Self-hosted Runner**.
   - Select the **Linux** runner image. Follow the commands provided on the page.

---

3. **Commands for Setting Up the Runner**:

#### a) **Download Section**:
   - Run the commands exactly as provided on the GitHub page, in your EC2 instance:
     ```bash
     mkdir actions-runner && cd actions-runner
     curl -o actions-runner-linux-x64-2.322.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-linux-x64-2.322.0.tar.gz
     tar xzf ./actions-runner-linux-x64-2.322.0.tar.gz
     ```

#### b) **Configure Section**:
   - Run the command to configure the runner. Press **Enter** to accept defaults for optional inputs:
     ```bash
     ./config.sh --url https://github.com/<owner>/<repository> --token <your-token>
     ```
   - During configuration:
     - **Name of the runner group**: Press **Enter** (default option).
     - **Name of the runner**: Provide the name used in `main.yaml` (`self-hosted`) or press **Enter** to skip.
     - **Labels for the runner**: Press **Enter** to skip (default labels: `self-hosted`, `Linux`, `X64`).
     - **Name of work folder**: Press **Enter** (default `_work`).

   - Upon completion, you will see:
     ```
     √ Runner successfully added
     √ Runner connection is good
     √ Settings Saved.
     ```

#### c) **Run the Runner**:
   - Start the runner using:
     ```bash
     ./run.sh
     ```

   - You’ll see confirmation:
     ```
     √ Connected to GitHub
     Current runner version: '2.322.0'
     Listening for Jobs
     ```

---

4. **Validation in GitHub**:
   - Go back to **GitHub Repository** > **Settings** > **Actions** > **Runners**.
   - The runner will appear as **Idle** and is ready to listen for any workflow triggered by changes in the repository.

---

5. **Integration with `main.yaml`**:
   - Ensure your `main.yaml` workflow uses the `self-hosted` runner:
     ```yaml
     Continuous-Deployment:
       needs: build-and-push-ecr-image
       runs-on: self-hosted
       steps:
         - name: Checkout Code
           uses: actions/checkout@v3
     ```

---

6. **Usage**:
   - After setting everything up, any **push** or **change** in your GitHub repository will trigger the runner to execute workflows specified in the repository.

---

The commands for stopping and removing containers to avoid name conflicts should ideally be added to your **`main.yaml` file** within the relevant job or step of your GitHub Actions workflow.

Here's how you can update your `main.yaml` file:

---

### **Where to Place the Cleanup Command**
You should add the cleanup command in the job where you're deploying the container, likely under the `Continuous Deployment` job. Place it before the `docker run` command to ensure any existing container with the same name is stopped and removed.

---

### **Updated YAML Example**
Here’s how your `Continuous Deployment` job might look after adding the cleanup step:

```yaml
Continuous-Deployment:
  needs: build-and-push-ecr-image
  runs-on: self-hosted
  steps:
    - name: Checkout Code
      uses: actions/checkout@v3

    - name: Stop and Remove Existing Container (if any)
      run: |
        docker ps -aq --filter "name=container-name" | xargs -r docker rm -f

    - name: Deploy the Docker Container
      run: |
        docker run -d -p 8080:8000 --ipc="host" \
          --name=container-name \
          -e 'AWS_ACCESS_KEY_ID=${{ secrets.AWS_ACCESS_KEY_ID }}' \
          -e 'AWS_SECRET_ACCESS_KEY=${{ secrets.AWS_SECRET_ACCESS_KEY }}' \
          -e 'AWS_REGION=${{ secrets.AWS_REGION }}' \
          image-repository-url:tag
```

---

### **Explanation of the Cleanup Command**
```bash
docker ps -aq --filter "name=container-name" | xargs -r docker rm -f
```
- **`docker ps -aq --filter "name=container-name"`**: Lists all containers with the specified name (`container-name`), whether they're running or stopped.
- **`xargs -r docker rm -f`**: Forcibly removes any container(s) returned by the above command.

By including this step in the YAML file, you ensure that any existing container with the same name is removed before a new one is deployed. This prevents deployment failures due to name conflicts.

---

### **Why Include It in `main.yaml`?**
- Automating this cleanup in the CI/CD pipeline avoids manual intervention and ensures smooth deployments every time.
- It centralizes all deployment-related commands in your GitHub Actions workflow for better visibility and management.

Here’s a well-structured note for you to review and revise later:

---

### **Configuring Security Group Inbound Rules for EC2**

After resolving all setup and deployment issues, follow these steps to ensure your EC2 instance is accessible on the required port:

1. **Navigate to Security Groups**:
   - Go to the AWS **EC2 Console**.
   - Select your **Instance ID**.
   - Under the **Security** tab, find and click on the attached **Security Group**.

2. **Edit Inbound Rules**:
   - Click **Edit Inbound Rules** in the Security Group.

3. **Set the Rules**:
   - **Type**: Select **Custom TCP**.
   - **Port Range**: Enter `8080` (this is the port exposed in the Docker container: `docker run -d -p 8080:8000`).
   - **Source**: Set to `0.0.0.0/0`. This allows access from all IP addresses. *(Use cautiously as it opens the port to the internet; for enhanced security, you can restrict this to specific IPs or ranges).*

4. **Save the Rules**:
   - Click **Save Rules** to apply the changes.

---

### **Notes**:
- **Purpose**: This configuration allows incoming traffic on port `8080` to reach your application hosted in the EC2 instance.
- **Security Consideration**: Using `0.0.0.0/0` opens the port to all IPs. For production environments, restrict the **Source** to trusted IPs or ranges.


---

### **Accessing Your Application on EC2**

1. **Navigate to Instance Details**:
   - Go to the **AWS EC2 Console**.
   - Select your **Instance ID**.

2. **Find the Public IPv4 Address**:
   - Locate the **Public IPv4 Address** under the instance details. Example: `3.90.160.53`.

3. **Access the Application**:
   - Open a web browser.
   - Enter the public IP address followed by `:8080` (the port your application is running on). Example:
     ```
     3.90.160.53:8080
     ```

   - This should open your application served through the Docker container.

---

### **Important Note**:
- Ensure that **inbound rules** in the security group allow traffic on port `8080` (type **Custom TCP**, port range `8080`, source `0.0.0.0/0`) for this to work.

This note covers everything you need to access your application from a browser. 