pipeline {
  agent any

  environment {
    TF_DIR = "terraform"
    ANSIBLE_DIR = "ansible"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Lint & Validate') {
      steps {
        sh '''
          cd $TF_DIR
          terraform fmt -check || true
          terraform init -input=false
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
        withAWS(credentials: 'aws-keys', region: 'us-east-1') {
          sh '''
            cd $TF_DIR
            terraform init -input=false
            terraform plan -out=plan.tfplan -input=false
            terraform show -json plan.tfplan > plan.json || true
            cd ..
            # expose plan as artifact logs if you want
          '''
        }
      }
    }

    stage('Manual Approval') {
      steps {
        input message: "Apply Terraform plan to create infra?", ok: "Apply"
      }
    }

    stage('Terraform Apply') {
      steps {
        withAWS(credentials: 'aws-keys', region: 'us-east-1') {
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
          python3 scripts/tf_to_inventory.py
          ls -l inventory.ini tf_output.json
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
        echo "Add simple curl checks here (optional)."
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
