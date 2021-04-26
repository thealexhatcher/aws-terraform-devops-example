import os
import subprocess
import logging
import json
import boto3

class terraform:

    def __init__( self, project_name, working_directory, aws_profile='default', environment=''):
        session = boto3.session.Session(profile_name=aws_profile)
        aws_region = session.region_name
        if environment == '':
            user_id = str(session.client('sts').get_caller_identity()['UserId']).split(':')[1].split('@')[0].replace('.','').lower()
            environment = user_id
        self.project_name = project_name
        self.working_directory = working_directory
        self.aws_region = aws_region
        self.aws_profile = aws_profile
        self.environment = environment
    
    def __terraform_process ( self, subcommand )
        opt_chdir = f'-chdir="{self.working_directory}"'
        print(f'running terraform subcommand: {subcommand}')
        process = subprocess.Popen(f'terraform {opt_chdir} {subcommand}', 
            stdout=subprocess.PIPE, 
            stderr = subprocess.PIPE, 
            universal_newlines=True, 
            shell = True )
        while process.poll() is None:
            stout, sterr = process.communicate()
            print(stout)
        return_code = process.poll()
        if return_code != 0:
            raise Exception(stderr)
        return stdout
    
    def apply( self )
        apply_opt_region = f'-var "aws_region={self.aws_region}"'
        apply_opt_profile = f'-var "aws_profile={self.aws_profile}"'
        apply_opt_environment = f'-var "environment={self.environment}"'

        print('apply terraform state change')
        self.__terraform_process(
            f'apply {self.apply_opt_region} {self.apply_opt_profile} {self.apply_opt_environment} -auto-approve -no-color')
    
    def destroy ( self )
        apply_opt_region = f'-var "aws_region={self.aws_region}"'
        apply_opt_profile = f'-var "aws_profile={self.aws_profile}"'
        apply_opt_environment = f'-var "environment={self.environment}"'
        print('destroying terraform state...')
        self.__terraform_process(
            f'destroy {apply_opt_region} {apply_opt_profile} {apply_opt_environment} -auto-approve -no-color')

            
    def init ( self, tf_state_name, tf_state_bucket, tf_state_table, tf_state_role_arn ):
        init_opt_bucket = f'-backend-config=bucket={tf_bucket}'
        init_opt_key = f'-backend-config=key={self.project_name }/{self.environment}/{tf_state_name}/terraform.tfstate'
        init_opt_region = f'-backend-config=region={self.aws_region}'
        init_opt_profile = f'-backend-config=region={self.aws_profile}'
        init_opt_ddb = f'-backend-config=dynamodb_table={tf_state_table}'
        init_opt_role = f'-backend-config=role_arn={tf_state_role_arn}'
        print( 'initializing terraform state...')
        self.__terraform_process(
            f'init {init_opt_bucket} {init_opt_key} {init_opt_region} {init_opt_profile} {init_opt_ddb} {init_opt_role} -no-color')
    
    def output ( self )
        print('fetching terraform state output...')
        output = self.__terraform_process(f'output -json -no-color')
        return json.loads(output)



