import json
from typing import List, Optional
from datetime import datetime
from ...domain.models import TrendAnalysis
from ...domain.repositories import TrendAnalysisRepository
from ...infrastructure.database import DatabaseConnection

class MySQLTrendAnalysisRepository(TrendAnalysisRepository):
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    def create(self, analysis: TrendAnalysis) -> TrendAnalysis:
        """Create a new trend analysis"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO trend_analysis 
                (user_id, category, region, analyzed_at, results, criteria)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    analysis.user_id,
                    analysis.category,
                    analysis.region,
                    analysis.analyzed_at,
                    json.dumps(analysis.results),
                    json.dumps(analysis.criteria) if analysis.criteria else None
                ))
                connection.commit()
                
                # Get the generated ID
                analysis.id = cursor.lastrowid
                return analysis
                
        except Exception as e:
            raise Exception(f"Error creating trend analysis: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_id(self, analysis_id: int) -> Optional[TrendAnalysis]:
        """Get trend analysis by ID"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM trend_analysis WHERE id = %s"
                cursor.execute(sql, (analysis_id,))
                result = cursor.fetchone()
                
                if result:
                    return self._map_to_trend_analysis(result)
                return None
                
        except Exception as e:
            raise Exception(f"Error getting trend analysis by ID: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_user(self, user_id: int) -> List[TrendAnalysis]:
        """Get all trend analyses for a user"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM trend_analysis WHERE user_id = %s ORDER BY analyzed_at DESC"
                cursor.execute(sql, (user_id,))
                results = cursor.fetchall()
                
                return [self._map_to_trend_analysis(row) for row in results]
                
        except Exception as e:
            raise Exception(f"Error getting trend analyses by user: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def update(self, analysis: TrendAnalysis) -> TrendAnalysis:
        """Update trend analysis"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                UPDATE trend_analysis 
                SET category = %s, region = %s, results = %s, criteria = %s
                WHERE id = %s
                """
                cursor.execute(sql, (
                    analysis.category,
                    analysis.region,
                    json.dumps(analysis.results),
                    json.dumps(analysis.criteria) if analysis.criteria else None,
                    analysis.id
                ))
                connection.commit()
                return analysis
                
        except Exception as e:
            raise Exception(f"Error updating trend analysis: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def delete(self, analysis_id: int) -> bool:
        """Delete trend analysis"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "DELETE FROM trend_analysis WHERE id = %s"
                cursor.execute(sql, (analysis_id,))
                connection.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            raise Exception(f"Error deleting trend analysis: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def _map_to_trend_analysis(self, row: dict) -> TrendAnalysis:
        """Map database row to TrendAnalysis object"""
        return TrendAnalysis(
            id=row['id'],
            user_id=row['user_id'],
            category=row['category'],
            region=row['region'],
            analyzed_at=row['analyzed_at'],
            results=json.loads(row['results']),
            criteria=json.loads(row['criteria']) if row['criteria'] else {}
        ) 