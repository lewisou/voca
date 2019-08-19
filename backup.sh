#!/bin/bash

rm voca.tar.gz
tar -czvf voca.tar.gz ./voca.db
scp ./voca.tar.gz myloc:
