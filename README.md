# CS 691 Final Project

by Derek Stratton

## Description

This is an update of a Go Fish game, originally from [here](https://rosettacode.org/wiki/Go_Fish/Python)
that has been refactored for Python 3. I also added documentation, testing, and deployment to the game.
The game is a console Go Fish game with a human and computer player.

## Testing

Tests were written in Python using the unittest framework. The tests achieve above 75% code coverage
and are automatically run through a GitHub Actions workflow when a push is made to this repository.

## Deployment 

Deployment is done through GitHub actions, where the game is containerized using Docker and stored 
in AWS's Elastic Container Registry (ECR). The game is also deployed using AWS's Elastic Container
Service (ECS). This deployment workflow is executed when a push is made to the repository.