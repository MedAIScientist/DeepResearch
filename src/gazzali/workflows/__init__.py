#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workflow Templates Module for Gazzali Research

This module provides preset workflow templates for common academic research tasks,
allowing users to quickly configure the system for specific research types.
"""

from .templates import (
    WorkflowTemplate,
    WorkflowType,
    get_workflow_template,
    list_available_workflows,
    LITERATURE_REVIEW_TEMPLATE,
    SYSTEMATIC_REVIEW_TEMPLATE,
    METHODOLOGY_COMPARISON_TEMPLATE,
    THEORETICAL_ANALYSIS_TEMPLATE,
)

__all__ = [
    'WorkflowTemplate',
    'WorkflowType',
    'get_workflow_template',
    'list_available_workflows',
    'LITERATURE_REVIEW_TEMPLATE',
    'SYSTEMATIC_REVIEW_TEMPLATE',
    'METHODOLOGY_COMPARISON_TEMPLATE',
    'THEORETICAL_ANALYSIS_TEMPLATE',
]
