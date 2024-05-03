# zoho

conda activate python3

conda info --envs

export PATH="/Users/shuningzhou/anaconda3/envs/python3/bin:$PATH"
echo $PATH

Persist PATH

echo 'export PATH="/Users/shuningzhou/anaconda3/envs/python3/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile

echo 'export PATH="/Users/shuningzhou/anaconda3/envs/python3/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
