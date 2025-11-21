pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        CONFIG_DIR = 'configs/devices'
        GENERATED_DIR = 'generated_configs'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Validate Configurations') {
            steps {
                echo 'Validating network configurations...'
                sh '''
                    . venv/bin/activate
                    for config_file in ${CONFIG_DIR}/*.yaml; do
                        echo "Validating $config_file..."
                        python scripts/config_validator.py "$config_file" || exit 1
                    done
                '''
            }
        }
        
        stage('Generate Configurations') {
            steps {
                echo 'Generating device configurations...'
                sh '''
                    . venv/bin/activate
                    mkdir -p ${GENERATED_DIR}
                    for config_file in ${CONFIG_DIR}/*.yaml; do
                        device_name=$(basename "$config_file" .yaml)
                        output_file="${GENERATED_DIR}/${device_name}.cfg"
                        echo "Generating config for $device_name..."
                        python scripts/config_generator.py "$config_file" "$output_file"
                    done
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --tb=short || exit 1
                '''
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving generated configurations...'
                archiveArtifacts artifacts: 'generated_configs/*.cfg', fingerprint: true
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo 'Deploying to staging environment (dry-run)...'
                withCredentials([
                    usernamePassword(credentialsId: 'staging-network-creds', 
                                   usernameVariable: 'NETWORK_USERNAME', 
                                   passwordVariable: 'NETWORK_PASSWORD'),
                    string(credentialsId: 'staging-enable-password', 
                          variable: 'NETWORK_ENABLE_PASSWORD')
                ]) {
                    sh '''
                        . venv/bin/activate
                        for config_file in ${CONFIG_DIR}/*.yaml; do
                            device_name=$(basename "$config_file" .yaml)
                            generated_config="${GENERATED_DIR}/${device_name}.cfg"
                            if [ -f "$generated_config" ]; then
                                echo "Deploying $device_name to staging..."
                                python scripts/config_deployer.py "$config_file" "$generated_config" --dry-run || true
                            fi
                        done
                    '''
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to production environment (dry-run)...'
                script {
                    def deploy = input message: 'Deploy to Production?', 
                                    parameters: [choice(choices: ['Yes', 'No'], 
                                                       name: 'Deploy', 
                                                       description: 'Confirm production deployment')]
                    if (deploy == 'Yes') {
                        withCredentials([
                            usernamePassword(credentialsId: 'production-network-creds', 
                                           usernameVariable: 'NETWORK_USERNAME', 
                                           passwordVariable: 'NETWORK_PASSWORD'),
                            string(credentialsId: 'production-enable-password', 
                                  variable: 'NETWORK_ENABLE_PASSWORD')
                        ]) {
                            sh '''
                                . venv/bin/activate
                                echo "⚠️  PRODUCTION DEPLOYMENT (DRY RUN MODE)"
                                for config_file in ${CONFIG_DIR}/*.yaml; do
                                    device_name=$(basename "$config_file" .yaml)
                                    generated_config="${GENERATED_DIR}/${device_name}.cfg"
                                    if [ -f "$generated_config" ]; then
                                        echo "Deploying $device_name to production..."
                                        python scripts/config_deployer.py "$config_file" "$generated_config" --dry-run || true
                                    fi
                                done
                            '''
                        }
                    } else {
                        echo 'Production deployment cancelled by user'
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check logs for details.'
        }
        unstable {
            echo 'Pipeline is unstable. Review test results.'
        }
    }
}

