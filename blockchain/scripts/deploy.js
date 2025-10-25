const hre = require('hardhat');
const fs = require('fs');
const path = require('path');

async function main() {
  // Get network name
  const network = hre.network.name;
  console.log(`Deploying to ${network}...`);
  
  await hre.run('compile');

  const DocumentVerification = await hre.ethers.getContractFactory('DocumentVerification');
  console.log('Deploying DocumentVerification...');
  const doc = await DocumentVerification.deploy();
  await doc.deployed();

  console.log(`DocumentVerification deployed to: ${doc.address} on ${network}`);

  // Save contract address for CI verification
  if (process.env.CI) {
    fs.writeFileSync('.deployed-address', doc.address);
  }

  // write address and abi to repo for backend usage
  const outDir = path.join(__dirname, '..', 'abi');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const contractInfo = {
    address: doc.address,
    abi: DocumentVerification.interface.format('json'),
    network: network,
    deploymentTime: new Date().toISOString()
  };

  fs.writeFileSync(
    path.join(outDir, 'DocumentVerification.json'),
    JSON.stringify(contractInfo, null, 2)
  );

  // Write network-specific deployment info
  const deploymentInfo = {
    network,
    address: doc.address,
    deploymentTime: new Date().toISOString()
  };

  const deploymentsPath = path.join(outDir, 'deployments.json');
  let deployments = {};
  
  if (fs.existsSync(deploymentsPath)) {
    deployments = JSON.parse(fs.readFileSync(deploymentsPath, 'utf8'));
  }
  
  deployments[network] = deploymentInfo;
  fs.writeFileSync(deploymentsPath, JSON.stringify(deployments, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
