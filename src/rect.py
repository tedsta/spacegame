#!/usr/bin/env python

def intersects(a, b):
    if a.position.x <= b.position.x+b.size.x and a.position.x+a.size.x >= b.position.x and\
       a.position.y <= b.position.y+b.size.y and a.position.y+a.size.y >= b.position.y:
        return True
    return False

def contains(rect, point):
    if rect.position.x <= point.x and rect.position.x+rect.size.x >= point.x and\
       rect.position.y <= point.y and rect.position.y+rect.size.y >= point.y:
           return True
    return False
