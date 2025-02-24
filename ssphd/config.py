import yaml
from dataclasses import dataclass
from pathlib import Path
import os
import pkg_resources
import shutil

@dataclass
class Paths:
    templates: str = "ssphd/assets/templates"
    css: str = "assets/css"
    js: str = "assets/js"
    fonts: str = "assets/fonts"
    refs: str = 'refs'
    csl: str = "assets/csl"
    meta: str = "assets/meta"
    output_html: str = "html"
    output_latex: str = "latex"

class Config:
    def __init__(self, config_file=None):
        self.package_path = pkg_resources.resource_filename('ssphd', '')
        self.default_templates_path = os.path.join(self.package_path, 'assets/templates')
        self.default_config_path = os.path.join(self.package_path, 'default.config.yaml')
        self.pandoc_data_dir = os.path.expanduser('~/.pandoc/templates')
        
        if not os.path.exists(self.pandoc_data_dir):
            os.makedirs(self.pandoc_data_dir)
            
        self.paths = Paths()
        
        # Load default config first
        self.load_config(self.default_config_path)
        
        # Override with user config if provided
        if config_file:
            self.validate_file(config_file)
            self.load_config(config_file)
            
        self._setup_templates()
    
    def validate_file(self, filepath):
        """Validate that a file exists and is accessible"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        if not os.path.isfile(filepath):
            raise ValueError(f"Path is not a file: {filepath}")
        if not os.access(filepath, os.R_OK):
            raise PermissionError(f"File is not readable: {filepath}")

    def _setup_templates(self):
        """Setup templates in pandoc's template directory"""
        for template in os.listdir(self.default_templates_path):
            src = os.path.join(self.default_templates_path, template)
            dst = os.path.join(self.pandoc_data_dir, template)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            
        if 'paths' in config:
            for key, value in config['paths'].items():
                if hasattr(self.paths, key):
                    setattr(self.paths, key, value)

    def get_path(self, name):
        return getattr(self.paths, name)

    def get_template_path(self, template_name):
        """Look for template in user directory first, then package templates"""
        user_template = os.path.join(self.get_path('templates'), template_name)
        print('yo')
        print(user_template)
        if os.path.exists(user_template):
            return user_template
        return template_name  # Return just the name for pandoc's template resolution
