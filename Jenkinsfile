pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t petrescue:v1 ."
            }
        }
        stage('Run Selenium Tests') {
            steps {
                echo "Run Selenium Tests"
                sh 'python3 -m pip install -r requirements.txt'
                sh 'python3 app.py &'
                sh 'sleep 5'
                sh 'python3 -m pytest -v'
            }
        }
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'dbhavana',
                                                  passwordVariable: '9949422313')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }
        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Push Docker Image to Docker Hub"
                sh "docker tag petrescue:v1 dbhavana/pet-rescue-app:new"
                sh "docker push dbhavana/pet-rescue-app:new"
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml --validate=false'
                sh 'kubectl apply -f service.yaml'
            }
        }
    }
    post {
        always {
            sh 'pkill -f "python3 app.py" || true'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
