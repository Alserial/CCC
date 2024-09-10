# Software System for Long-term Health Analysis - Big Data Analytics on the Cloud
## By Group 32
Our team is made up by the following:

- Yucheng Luo     <1153247>  <stluo@student.unimelb.edu.au>
- Yiyang Huang    <1084743>  <yiyahuang@student.unimelb.edu.au>
- Jiaqi Fan       <1266359>  <jffan2@student.unimelb.edu.au>
- Yingying Zhong  <1158586>  <yizhong1@student.unimelb.edu.au>
- Mingyao Ke      <1240745>  <mingyaok@student.unimelb.edu.au>


## Contents

This is the formal repository for the COMP90024 Cluster and Cloud Computing Project 2 by group 32. This project provides a insightful data display and analysis on the topic of long-term health with some other integrated features. A real-time model is embedded in our back-end, providing insights on the importance of the features from various aspects including Weather observations, Income levels and Cultural customs.


### doc
This folder contains our fianl report and the API documents

### fission
This folder contains the back-end code, including all the functions depoyed in fission and corresponding specifications

### local_data_harvest
This folder contains code of the data harvest functions that operates locally for testing purpose. There is also local data included.

### local_model
This folder contains code of the modelling functions that operates locally for testing purpose. 

### frontend.ipynb
This notebook presents as the front-end, displaying key insights of our findings.

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

## Installation Instruction

### Front-end 
1. Connect to Unimelb VPN

2. Run the following command after obtaining the Kube Config file: 

`kubectl port-forward service/router -n fission 9099:80`

3. Install required local packages by running the following command:

`pip install -r requirements.txt`

4. Go to the `frontend.ipynb` and run as instructed.

### Back-end
1. Ensure `kubectl` and `fission` are installed. 

2. To apply specification, run `fission spec apply --specdir fission/specs --wait`


## Citation
If you find this repo helpful, please cite our project.

```
@article{long-term-health-cloud,
  title={Software System for Long-term Health Analysis - Big Data Analytics on the Cloud},
  author={Luo, Yuchen and Huang, Yiyang and Fan, Jiaqi and Zhong, Yingying and Ke, Mingyao},
  year={2024}
}
```