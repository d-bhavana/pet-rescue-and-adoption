pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                bat "docker build -t petrescue:v1 ."
            }
        }


     
  stage('Run Tests') {
    steps {
        bat '''
        docker run --rm petrescue:v1 sh -c "
        python app.py &
        sleep 5 &&
        pytest -v
        "
        '''
    }
}
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
    credentialsId: 'dockerhub-creds',
    usernameVariable: 'DOCKER_USER',
    passwordVariable: 'DOCKER_PASS'
)]) {
    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
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
