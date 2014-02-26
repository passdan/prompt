#!/bin/bash

sudo rm -r /var/www/prompt/analyses/abun/SEQ/*
sudo cp -r tmp_dir/abundance_files/* /var/www/prompt/analyses/abun/SEQ/

sudo rm -r /var/www/prompt/analyses/pie/SEQ/*
sudo cp -r tmp_dir/html_files/* /var/www/prompt/analyses/pie/SEQ/
