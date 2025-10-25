import subprocess
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Deploy the DocumentVerification smart contract using Hardhat and write ABI/address to blockchain/abi/'

    def handle(self, *args, **options):
        cwd = os.path.join(os.path.dirname(__file__), '..', '..')  # blockchain folder
        self.stdout.write('Running npm install (if needed) and deploying contract...')
        try:
            subprocess.check_call(['npm', 'install', '--no-audit', '--no-fund', '--legacy-peer-deps'], cwd=cwd)
            subprocess.check_call(['npm', 'run', 'deploy:hardhat'], cwd=cwd)
        except subprocess.CalledProcessError as e:
            self.stderr.write(f'Error running deploy: {e}')
            return

        addr_file = os.path.join(cwd, 'abi', 'contract-address.txt')
        if os.path.exists(addr_file):
            with open(addr_file, 'r') as f:
                address = f.read().strip()
            self.stdout.write(self.style.SUCCESS(f'Contract deployed to: {address}'))
        else:
            self.stdout.write(self.style.WARNING('Contract address file not found.'))
