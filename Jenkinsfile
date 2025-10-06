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
      steps {
        withCredentials([file(credentialsId: 'BACKEND_SECRET', variable: 'BACKEND_FILE')]) {
          sh '''
        cp "${BACKEND_FILE}" "${TF_DIR}/backend.hcl"
        cat "${TF_DIR}/backend.hcl"
        '''
        }
      }
    }

    stage('Lint & Validate') {
      steps {
        sh '''
          cd $TF_DIR
          terraform fmt -check || true
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
            terraform init -backend-config=backend.hcl
            terraform plan -out=plan.tfplan
            terraform show -json plan.tfplan > plan.json || true
            cd ..
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
            terraform output -json > tf_output.json
            cd ..
          '''
        }
      }
    }

    stage('Generate Inventory') {
      steps {
        sh '''
          echo "=== Terraform Output ==="
          cd $TF_DIR
          ls -l tf_output.json
          cat tf_output.json

          echo "=== Generating Ansible Inventory ==="
          python3 ../scripts/tf_to_inventory.py

          echo "=== Inventory Created ==="
          ls -l inventory.ini
          cat inventory.ini

          # Copy inventory to workspace root for Ansible stage
          cp inventory.ini ../inventory.ini
          cd ..
        '''
      }
    }

    stage('Ansible Configure') {
      steps {
        withCredentials([sshUserPrivateKey(credentialsId: 'ansible-ssh-key', keyFileVariable: 'SSH_KEYFILE')]) {
          sh '''
            chmod 600 $SSH_KEYFILE
            echo "=== Using Inventory ==="
            cat inventory.ini
            echo "=== Running Ansible Playbook ==="
            ansible-playbook -i inventory.ini --private-key $SSH_KEYFILE $ANSIBLE_DIR/playbook.yml
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
