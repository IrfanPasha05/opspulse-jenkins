pipeline {

    agent any

    environment {
        APP_NAME   = 'opspulse'
        APP_PORT   = '5000'
        DEPLOY_DIR = '/opt/opspulse'
        VENV_DIR   = 'venv'
        PID_FILE   = 'opspulse.pid'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '======================================'
                echo 'Checking out OpsPulse from GitHub...'
                echo '======================================'
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
                echo '======================================'
                echo 'Running automated tests...'
                echo '======================================'

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
                        --exclude=./venv \
                        --exclude=./.git \
                        -czf opspulse-${BUILD_NUMBER}.tar.gz .
                '''

                archiveArtifacts artifacts: "opspulse-${BUILD_NUMBER}.tar.gz",
                                 fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                echo '======================================'
                echo 'Deploying OpsPulse to EC2...'
                echo '======================================'

                sh '''
                    # Create deployment directory
                    sudo mkdir -p ${DEPLOY_DIR}

                    # Copy application files
                    sudo cp app.py ${DEPLOY_DIR}/
                    sudo cp requirements.txt ${DEPLOY_DIR}/

                    # Copy templates
                    sudo mkdir -p ${DEPLOY_DIR}/templates
                    sudo cp -r templates/. ${DEPLOY_DIR}/templates/

                    # Create deployment virtual environment
                    sudo python3 -m venv ${DEPLOY_DIR}/venv

                    # Give Jenkins ownership of deployment files
                    sudo chown -R jenkins:jenkins ${DEPLOY_DIR}

                    # Install production dependencies
                    ${DEPLOY_DIR}/venv/bin/pip install \
                        -r ${DEPLOY_DIR}/requirements.txt

                    # Restart application
                    sudo systemctl restart ${APP_NAME}

                    # Show service status
                    sudo systemctl --no-pager status ${APP_NAME} || true
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo '======================================'
                echo 'Checking OpsPulse health...'
                echo '======================================'

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
            echo '       OPSSPULSE DEPLOYMENT SUCCESS'
            echo '======================================'
            echo "OpsPulse is running on port ${APP_PORT}"
            echo "Build number: ${BUILD_NUMBER}"
        }

        failure {
            echo '======================================'
            echo '       OPSSPULSE DEPLOYMENT FAILED'
            echo '======================================'
            echo 'Check the failed stage above.'

            sh '''
                echo "----- Service Status -----"
                sudo systemctl --no-pager status ${APP_NAME} || true

                echo "----- Recent Service Logs -----"
                sudo journalctl -u ${APP_NAME} -n 50 --no-pager || true
            '''
        }

        always {
            echo "Jenkins build completed: ${BUILD_NUMBER}"
        }
    }
}
