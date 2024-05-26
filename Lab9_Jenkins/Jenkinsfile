pipeline {
    agent any

    stages {
        stage('Stage 0: Clone Repo') {
            steps {
                echo 'Cloning..'
		git branch: 'main', credentialsId: '3464aa34-c94d-42d6-9cd7-fdfec72319ab', url: 'https://github.com/Logan-Chayet/Lab9.git'
            }
        }
        stage('Stage 1: Install Packages') {
            steps {
                echo 'Installing..'
		sh 'pip3 install --upgrade ncclient pandas netaddr prettytable'
            }
        }
        stage('Stage 2: Checking and Fixing Violations') {
            steps {
		script {
			echo 'Checking for erros....'
			def pylint = sh(script: 'pylint --fail-under=5 /var/lib/jenkins/workspace/Lab9/Lab9.py', returnStatus: true)
			if (pylint != 0) { 
				error 'Pylint score <5. Please fix to increase score.'
			}
		}
            }
        }
	stage('Stage 3: Run the Application') {
            steps {
                echo 'Running..'
		sh 'python3 /var/lib/jenkins/workspace/Lab9/Lab9.py'
            }
        }
	stage('Stage 4: Unit Test') {
            steps {
                echo 'Testing..'
                sh 'python3 /var/lib/jenkins/workspace/Lab9/unitTest.py'
            }
        }
    }
    post {
	always {
		emailext body: '$DEFAULT_CONTENT', 
		recipientProviders: [
		    [$class: 'CulpritsRecipientProvider'],
		    [$class: 'DevelopersRecipientProvider'],
		    [$class: 'RequesterRecipientProvider']
		], 
		replyTo: '$DEFAULT_REPLYTO', 
		subject: '$DEFAULT_SUBJECT',
		to: '$DEFAULT_RECIPIENTS'
	}
    }
}
