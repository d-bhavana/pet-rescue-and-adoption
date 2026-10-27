pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                bat "docker build -t petrescue:v1 ."
            }
        }
        stage('Run Selenium Tests') {
            steps {
                echo "Run Selenium Tests"
                bat 'python -m pip install -r requirements.txt'
                bat 'python app.py &'
                bat 'sleep 5'
                bat 'python -m pytest -v'
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'dbhavana',
                                                  passwordVariable: '9949422313')]) {
                    bat 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }
        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Push Docker Image to Docker Hub"
                bat "docker tag petrescue:v1 dbhavana/pet-rescue-app:new"
                bat "docker push dbhavana/pet-rescue-app:new"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }
    post {
       always {
            bat(returnStatus: true, script: '''for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5001 ^| findstr LISTENING') do taskkill /F /PID %%a''')
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
