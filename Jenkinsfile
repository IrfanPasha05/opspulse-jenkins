pipeline {

    agent any

    environment {
        APP_NAME = 'opspulse'
        APP_PORT = '5000'
        VENV_DIR = 'venv'
        DEPLOY_DIR = '/opt/opspulse'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out OpsPulse from GitHub...'
                checkout scm
            }
        }

        stage('Python Environment') {
            steps {
                echo 'Creating Python virtual environment...'

                sh '''
                    python3 --version

                    python3 -m venv ${VENV_DIR}

                    . ${VENV_DIR}/bin/activate

                    python -m pip install --upgrade pip

                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running automated tests...'

                sh '''
                    . ${VENV_DIR}/bin/activate

                    python -m pytest -v

              '''
           }
        }

        stage('Build Artifact') {
            steps {
                echo 'Creating deployment artifact...'

                sh '''
                    tar \
                    --exclude='./venv' \
                    --exclude='./.git' \
                    -czf opspulse-${BUILD_NUMBER}.tar.gz .
                '''

                archiveArtifacts artifacts: 'opspulse-*.tar.gz',
                                 fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying OpsPulse to EC2...'

                sh '''
                    sudo mkdir -p ${DEPLOY_DIR}

                    sudo cp app.py ${DEPLOY_DIR}/
                 
                   sudo cp requirements.txt ${DEPLOY_DIR}/

                   sudo cp -r templates ${DEPLOY_DIR}/
                    
                    sudo python3 -m venv ${DEPLOY_DIR}/venv

                     ${DEPLOY_DIR}/venv/bin/pip install \
                        -r ${DEPLOY_DIR}/requirements.txt

                    sudo chown -R jenkins:jenkins ${DEPLOY_DIR}

                    sudo systemctl restart ${APP_NAME}
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo 'Checking application health...'

                sh '''
                    sleep 3

                    curl -f http://127.0.0.1:${APP_PORT}/health
                '''
            }
        }
    }

    post {

        success {
            echo '======================================'
            echo '       OPSSPULSE DEPLOYED'
            echo '======================================'
            echo "Application: ${APP_NAME}"
            echo "Port: ${APP_PORT}"
            echo 'Status: HEALTHY'
        }

        failure {
            echo '======================================'
            echo '       OPSSPULSE DEPLOYMENT FAILED'
            echo '======================================'
            echo 'Check the failed stage above.'
        }
    }
}
