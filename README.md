This branch is to be used strictly for deploy testing. Master will contain all, fully functional code, deploy-testing will contain all code that is ready to be tested after deploying (and any subseqeuent debugging), any other branch will be for the current development cycle.

deploy-testing will not, under any circumstances barring the archiving of the project, be merged into master. If something is tested and fully functional for master, use the following commands to update the master branch:

git checkout master
git pull origin master
git merge deploy-testing
git push origin master