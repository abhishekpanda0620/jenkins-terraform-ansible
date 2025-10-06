pipeline {
  agent any

  environment {
    TF_DIR = 'terraform'
    ANSIBLE_DIR = 'ansible'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('setup backend.hcl') {
      withCredentials([string(credentialsId: 's3-bucket-name', variable: 'S3_BUCKET_NAME')]) {
        withCredentials([string(credentialsId: 'aws-region', variable: 'AWS_REGION')]) {
          steps {
            sh '''
              cd $TF_DIR
              echo "bucket         = \\"${S3_BUCKET_NAME}\\"" > backend.hcl
              echo "region         = \\"${AWS_REGION}\\"" >> backend.hcl
              terraform init -backend-config=backend.hcl
              cd ..
            '''
          }
        }
      }
    }

    stage('Lint & Validate') {
      steps {
        sh '''
          cd $TF_DIR
          terraform fmt -check || true
          terraform init -backend-config=backend.hcl
          terraform validate || true
          cd ..
          # optional: ansible-lint
          if command -v ansible-lint >/dev/null 2>&1; then
            ansible-lint $ANSIBLE_DIR/playbook.yml || true
          fi
        '''
      }
    }

    stage('Terraform Plan') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'aws-keys', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
          sh '''
            cd $TF_DIR
            terraform init
            terraform plan -out=plan.tfplan
            terraform show -json plan.tfplan > plan.json || true
            cd ..
            # expose plan as artifact logs if you want
          '''
        }
      }
    }

    stage('Terraform Apply') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'aws-keys', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
          sh '''
            cd $TF_DIR
            terraform apply -auto-approve plan.tfplan
            terraform output -json > ../tf_output.json
            cd ..
          '''
        }
      }
    }

    stage('Generate Inventory') {
      steps {
        sh '''
      echo "Listing Terraform output file:"
      ls -l ../tf_output.json
      cat ../tf_output.json || true
      python3 scripts/tf_to_inventory.py
      ls -l inventory.ini
      cat inventory.ini || true
    '''
      }
    }

    stage('Ansible Configure') {
      steps {
        // SSH key stored in Jenkins as "SSH Username with private key" credential type
        withCredentials([sshUserPrivateKey(credentialsId: 'ansible-ssh-key', keyFileVariable: 'SSH_KEYFILE')]) {
          sh '''
            chmod 600 $SSH_KEYFILE
            ansible-playbook -i inventory.ini -u ubuntu --private-key $SSH_KEYFILE ansible/playbook.yml
          '''
        }
      }
    }

    stage('Smoke Test') {
      steps {
        echo 'Add simple curl checks here (optional).'
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'tf_output.json, inventory.ini', allowEmptyArchive: true
      cleanWs()
    }
  }
}
