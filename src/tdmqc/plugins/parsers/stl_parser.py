"""
STL Parser Plugin for 3DModelQuickCalc
Reads STL files and extracts basic geometry information
"""

import trimesh
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class STLParser:
    """Parser for STL (Stereolithography) 3D files"""
    
    def __init__(self):
        self.supported_formats = ['.stl']
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse an STL file and return geometry information
        
        Args:
            file_path: Path to the STL file
            
        Returns:
            Dictionary with parsing results
        """
        try:
            logger.info(f"Parsing STL file: {file_path}")
            
            # Load the mesh using trimesh
            mesh = trimesh.load(file_path)
            
            # Calculate basic properties
            result = {
                "success": True,
                "file": file_path,
                "vertices": len(mesh.vertices),
                "faces": len(mesh.faces),
                "volume": float(mesh.volume) if hasattr(mesh, "volume") else 0.0,
                "bounds": mesh.bounds.tolist() if hasattr(mesh, "bounds") else [],
                "center_of_mass": mesh.center_mass.tolist() if hasattr(mesh, "center_mass") else [0, 0, 0],
                "is_watertight": bool(mesh.is_watertight) if hasattr(mesh, "is_watertight") else False
            }
            
            logger.info(f"STL parsed successfully: {result['vertices']} vertices, {result['faces']} faces")
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse STL file {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "file": file_path
            }
    
    def validate(self, file_path: str) -> bool:
        """Validate if file is a valid STL"""
        try:
            mesh = trimesh.load(file_path)
            return len(mesh.vertices) > 0 and len(mesh.faces) > 0
        except:
            return False

# Пример использования (для тестов)
if __name__ == "__main__":
    parser = STLParser()
    
    # Тестовый куб
    test_mesh = trimesh.creation.box([10, 10, 10])
    test_mesh.export("test_cube.stl")
    
    result = parser.parse("test_cube.stl")
    print("Test parse result:", result)