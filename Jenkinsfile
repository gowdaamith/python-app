pipeline {
    agent { label 'linux' }

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    parameters {
        choice(name: 'ENV', choices: ['dev', 'stage', 'prod'], description: 'Select Environment')
        string(name: 'APP_VERSION', defaultValue: "v1.0.${BUILD_NUMBER}", description: 'App Version')
    }

    environment {
        APP_NAME = "Python-flask-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git(
                    branch: 'main',
                    url: 'https://github.com/gowdaamith/python-app.git',
                    credentialsId: 'git-token'
                )
            }
        }
        stage('Install dependencies') {
            steps {
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }
        stage('Run tests') {
            steps {
                sh 'pytest || true'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t gowdaamith/${APP_NAME}:${params.APP_VERSION} ."
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo \$PASS | docker login -u \$USER --password-stdin"
                    sh "docker push gowdaamith/${APP_NAME}:${params.APP_VERSION}"
                }
            }
        }

        stage('Approval') {
            when { branch 'main' }
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    input message: "Approve Deployment to ${params.ENV}?"
                }
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['Ec2access']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@13.204.143.172 "
                            docker pull gowdaamith/${APP_NAME}:${params.APP_VERSION} &&
                            docker stop ${APP_NAME} || true &&
                            docker rm ${APP_NAME} || true &&
                            docker run -d --name ${APP_NAME} -p 5000:5000 \
                                -e APP_VERSION=${params.APP_VERSION} \
                                -e ENVIRONMENT=${params.ENV} \
                                gowdaamith/${APP_NAME}:${params.APP_VERSION}
                        "
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully! Version: ${params.APP_VERSION}"
        }
        failure {
            echo "Pipeline failed!"
        }
        always {
            cleanWs()
        }
    }
}

