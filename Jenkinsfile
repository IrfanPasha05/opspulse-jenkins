pipeline {

    agent any

    environment {
        APP_NAME   = 'opspulse'
        APP_PORT   = '5000'
        DEPLOY_DIR = '/opt/opspulse'
        VENV_DIR   = 'venv'
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

                    rm -rf ${VENV_DIR}

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
                echo '======================================'
                echo 'Creating deployment artifact...'
                echo '======================================'

                sh '''
                    rm -f opspulse-*.tar.gz

                    tar \
                        --exclude='./venv' \
                        --exclude='./.git' \
                        --exclude='./opspulse-*.tar.gz' \
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
                    sudo mkdir -p ${DEPLOY_DIR}

                    sudo cp app.py ${DEPLOY_DIR}/
                    sudo cp requirements.txt ${DEPLOY_DIR}/

                    sudo mkdir -p ${DEPLOY_DIR}/templates
                    sudo cp -r templates/. ${DEPLOY_DIR}/templates/

                    sudo python3 -m venv ${DEPLOY_DIR}/venv

                    sudo chown -R jenkins:jenkins ${DEPLOY_DIR}

                    ${DEPLOY_DIR}/venv/bin/pip install \
                        -r ${DEPLOY_DIR}/requirements.txt

                    sudo systemctl restart ${APP_NAME}

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
            echo "Application: ${APP_NAME}"
            echo "Port: ${APP_PORT}"
            echo "Build: ${BUILD_NUMBER}"
            echo 'Health Check: PASSED'
        }

        failure {
            echo '======================================'
            echo '       OPSSPULSE DEPLOYMENT FAILED'
            echo '======================================'
            echo "Failed Build: ${BUILD_NUMBER}"

            sh '''
                echo "----- OpsPulse Service Status -----"
                sudo systemctl --no-pager status ${APP_NAME} || true
            '''
        }

        always {
            echo "Jenkins build completed: ${BUILD_NUMBER}"
        }
    }
}
