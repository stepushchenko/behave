# Installation Behave Project One on Ubuntu 20.04

### Installation Docker
https://docs.docker.com/engine/install/ubuntu/ 

### Installation Java 11
```bash
java -version
sudo apt-get update
sudo apt-get install openjdk-11-jdk
java -version
```

### Installation Jenkins
```bash
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins
```

### Installation Selenoid
```bash
curl -s https://aerokube.com/cm/bash | bash
chmod +x cm
./cm selenoid start
```

### Installation Venv
```bash
sudo apt install python3.8-venv
```

### Installation AWS client
```bash
sudo apt-get install awscli
```

### Clone repository from GitHub
```bash
git clone git@github.com:yourcoach/tests.git
```

### Installation Requirements (tests directory)
```bash
apt install python3-pip
pip install -r requirements.txt
```

### Activate Venv (tests directory)
```bash
. env/bin/activate
```

### PYTHONPATH
Update PATH if necessary <br>
Update PYTHONPATH if necessary

## What's inside

1. `Selenoid` is required for run tests on different browser versions
2. `Jenkins` is required for managing CI/CD process
3. `Java` is required for Jenkins
4. `Docker` is required for Selenoid
5. `Behave` is required for BDD framework implementation
6. `BehaveX` is required for run tests in parallel processes
7. `Behave-html-formatter`is required for simple html reports generation
8. `Boto3` is required for AWS integration
9. `Slack-sdk` is required for Slack integration

## Run tests

Run all tests with `behave` library
```bash 
behave
```

Run specific scenario with `behave` library
```bash
bahave -n "[scenario_name]"
# example
behave -n "search imgs of Alpine cows"
```

Run specific feature with `behave` library
```bash
behave -i [feature_name.feature]
# example
behave -i google.feature
```

Run all tests in parallel with `behavex` library
```bash 
behavex --parallel-processes [count_of_parallel_processes]
# example
behavex --parallel-processes 5
```

Run all tests with reports with `behave-html-formatter` library
```bash
behave -f html -o [path_to_the_reports_directory]/[report_file.html] features
# example
behave -f html -o reports/html/report.html features
```

Run specific feature with reports with `behave-html-formatter` library
```bash
behave -f html -o [path_to_the_reports_directory]/[report_file.html] features/[feature_name.feature]
# example
behave -f html -o reports/html/report.html features/google.feature
```
