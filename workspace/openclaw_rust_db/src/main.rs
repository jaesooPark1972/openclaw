use sqlx::postgres::PgPoolOptions;
use dotenvy::dotenv;
use std::env;

#[tokio::main]
async fn main() -> Result<(), anyhow::Error> {
    dotenv().ok();

    // 1. Connection String (D:/OpenClaw/.env 정보를 활용)
    // 텔레그램 대화 내역이나 프로젝트 메타데이터를 저장할 용도라고 가정
    let database_url = "postgres://postgres:2903@localhost:5432/openclaw_db";

    println!("🌐 [Rust-DB] Connecting to openclaw_db (Stored on Google Drive)...");

    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(database_url)
        .await?;

    println!("✅ [Rust-DB] Connection Successful!");

    // 2. 초기 테이블 생성 (예: 시스템 로그 또는 에이전트 상태)
    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS agent_memory (
            id SERIAL PRIMARY KEY,
            agent_name TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
        "#
    )
    .execute(&pool)
    .await?;

    println!("📊 [Rust-DB] 'agent_memory' table initialized.");

    // 3. 테스트 데이터 삽입
    sqlx::query(
        "INSERT INTO agent_memory (agent_name, content) VALUES ($1, $2)"
    )
    .bind("jayhomebot")
    .bind("System successfully migrated to Google Drive backed PostgreSQL.")
    .execute(&pool)
    .await?;

    let row: (i64,) = sqlx::query_as("SELECT COUNT(*) FROM agent_memory")
        .fetch_one(&pool)
        .await?;

    println!("📈 [Rust-DB] Total memories stored: {}", row.0);

    Ok(())
}
