# Environmental monitoring platform based on Raspberry Pi and Django

## Tech stack

- 🍓Raspberry Pi

- 💦DHT11
- 🦟MQTT
- 🐍Python
- 🛠️Django
- ⚡️JavaScript
- 🚗Echarts
- ☁️AWS (IoT Core, Lambda, RDS, VPC, EC2)
- 🧘Restful API
- 🥋Nginx
- ⚙️wsgi

## Introduction

We developed this platform using Raspberry Pi and DHT11 to complete the detection of temperature and humidity in the environment. We used the MQTT protocol to send the data to the AWS IoT client. We created AWS Lambda expressions and passed the data to AWS RDS (PostgreSQL) for data storage. A Django web application deployed on AWS EC2 relying on Nginx and wsgi reads the data from the database and visualizes it using Echarts. Also, we implemented the Restful API to control the sensors connected to the Raspberry Pi and integrated the functionality in the web application.

This project contains two parts:

Django web application part: https://github.com/Szzx123/PlatformIoT-Environment-RaspberryPi-Django-AWS-Web

Monitoring data and API listening to sensor status in Raspberry Pi part: https://github.com/Szzx123/PlatformIoT-Environment-RaspberryPi

### Web Application Overview

Login Page

<img src="./IMG/1.png" alt="1"  />

Main Page

<img src="./IMG/2.png" alt="2"  />

Temperature Dashboard

<img src="./IMG/3.png" alt="3"  />

Humidity Dashboard

<img src="./IMG/4.png" alt="4"  />

Devices Control

<img src="./IMG/5.png" alt="5"  />

<img src="./IMG/6.png" alt="6"  />

### Structure

<img src="./IMG/7.png" alt="7" style="zoom: 50%;" />

The diagram above shows the structure of our project. First, on the Raspberry Pi side, it collects data from the DHT11 connected to it, and then transmits it via the MQTT protocol to the IOT Core MQTT client in the AWS cloud service.

We then created a rule in the AWS IOT so that whenever it receives data, it triggers AWS Lambda, using Lambda to transmit the data into the AWS RDS database in the VPC we created.

In order to provide an interactive interface for sensor management and visualization, we developed a web application using Django and Python, which was deployed on an AWS EC2 instance by nginx + uwsgi and read the data stored in the RDS.

With the NAT configured by the VPC, we can access this web application from the public network. Finally, to implement functions related to control, adding sensors, etc., we created RESTful APIs in Django for the Raspberry Pi to access and execute commands.

## Getting started

### Setting up Raspberry Pi and AWS IoT

You can refer to the following tutorial for configuration: https://docs.aws.amazon.com/iot/latest/developerguide/connecting-to-existing-device.html

After you have configured the environment on the Raspberry Pi side, you can use our code to send data to the IoT Core.

In your Raspberry Pi terminal:

```bash
git pull https://github.com/Szzx123/PlatformIoT-Environment-RaspberryPi.git
cd PlatformIoT-Environment-RaspberryPi
python3 AWS_DHT_RPI.py
--topic device/3/data --ca_file ~/Desktop/mqtt/AmazonRootCA1.pem
--cert ~/Desktop/mqtt/certificate.pem.crt
--key ~/Desktop/mqtt/private.pem.key
--endpoint a3vf4f15xaiiy7-ats.iot.eu-west-3.amazonaws.com
--device_id 3 --gpio 4 --count 10000
```

`--topic` is an event that we and AWS IOT need to subscribe to together and AWS IOT rules can receive data under the same event and operate it.

The `--ca_file`, `--cert`, `--key` parameters are the provided certificates and keys we need to use our own AWS cloud service, which ensures security. And --count represents the number of times we want to read the data.

`--device_id` is the number you want to set for the DHT11, it can be any number. `--gpio` is the gpio number of your DHT11 connected to the Raspberry Pi. `--count` is the number of times to send data to IoT Core.