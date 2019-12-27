pipeline {
    agent any
    environment {
        scannerHome='/opt/sonar-scanner/bin/sonar-scanner'
    }
    
    stages {
        //stage('clone') {
        //    steps {
        //        git branch: 'kishore', url: 'https://github.com/kishore1512/ZUCK.git'
        //    }
        //}
        stage('SonarQube analysis') {
            steps {
                //def scannerHome = tool 'Sonar-Scanner';
                //withSonarQubeEnv('sonar') { // If you have configured more than one global server connection, you can specify its name
                sh "${scannerHome} -Dsonar.projectKey=py   -Dsonar.sources=.   -Dsonar.host.url=https://sonar.kishorereddy.tk   -Dsonar.login=3d9faad0dc57b404bcf5a97bca5a3c9ae3b7720f"
                } 
            }
        stage("Quality Gate") {
            steps {
                sh ''' 
                    export AWS_DEFAULT_REGION="us-east-1"
                    export APP_NAME="ZUCK"
                    export ENV_NAME="python-sonar-sample"
                    export S3_BUCKET="zuck-dev"
                    export APP_VERSION=`git rev-parse --short HEAD`
                    fail_check () {
                        if [ $? -ne 0 ]
                        then
                            echo "Failed"
                            exit 1
                        fi
                    }
                    #Create EBS package
                    { set +x; } 2>/dev/null
                    printf "\n\n##### Zip up package to deploy to EBS #####\n"
                    git clean -fd
                    zip -x *.git* -r "${APP_NAME}-${APP_VERSION}.zip" .
                    #Deploy EBS package
                    aws elasticbeanstalk delete-application-version --application-name "${APP_NAME}" --version-label "${APP_VERSION}"  --delete-source-bundle
                    aws s3 cp ${APP_NAME}-${APP_VERSION}.zip s3://${S3_BUCKET}/${APP_NAME}-${APP_VERSION}.zip
                    aws elasticbeanstalk create-application-version --application-name "${APP_NAME}" --version-label "${APP_VERSION}" --source-bundle S3Bucket="${S3_BUCKET}",S3Key="${APP_NAME}-${APP_VERSION}.zip"
                    aws elasticbeanstalk update-environment --environment-name "${ENV_NAME}" --version-label "${APP_VERSION}"
                    #sleep before checking health of the app
                    sleep 60
                    #Check on application status
                    { set +x; } 2>/dev/null
                    printf "\n\n##### Check EBS environment health #####\n"
                    for ((j=1;j<=30;j++))
                    do
                    HealthStatus="$(aws elasticbeanstalk describe-environment-health --environment-name "${ENV_NAME}" --attribute-names HealthStatus --output=text | awk '{print $2}')"
                    fail_check
                    if [[ "$HealthStatus" == "Ok" ]]
                    then
                        for ((k=1;k<=10;k++))
                        do
                            sleep 6
                            HealthStatus="$(aws elasticbeanstalk describe-environment-health --environment-name "${ENV_NAME}" --attribute-names HealthStatus --output=text | awk '{print $2}')"
                            fail_check
                            if [ $k -eq 10 ] && [[ "$HealthStatus" == "Ok" ]]
                            then
                                echo "Environment is healthy"
                                #Check deployed version
                                DeployedAppVersion="$(aws elasticbeanstalk describe-environments --environment-names "${ENV_NAME}" --query 'Environments[0].VersionLabel' --output=text)"
                                fail_check
                                if [[ "$DeployedAppVersion" != "$APP_VERSION" ]]
                                then
                                    echo "But current version $APP_VERSION deployment failed and restored to previous version $DeployedAppVersion"
                                    exit 1
                                fi
                                #Display AWS EBS endpoint
                                printf "Deployed the new version $DeployedAppVersion successfully"
                                break 2
                            else
                                if [ $k -ne 10 ] && [[ "$HealthStatus" == "Ok" ]]
                                then
                                    continue
                                fi
                                echo "Environment is unstable"
                                j=$(($j-1))
                                break
                            fi
                        done
                    else
                        echo "Environment is not healthy, checking after 1 minute"
                        sleep 60
                        if [ $j -eq 30 ]
                        then
                            if [[ "$HealthStatus" == "Info" ]] || [[ "$HealthStatus" == "Pending" ]]
                            then
                                j=1
                                echo "Environment is still in $HealthStatus state"
                            else
                                echo "Environment is in $HealthStatus state"
                                exit 1
                            fi
                        fi
                    fi
                    done
                '''    
            }
        }
    }
}
