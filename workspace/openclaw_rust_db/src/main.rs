use sqlx::postgres::PgPoolOptions;
use dotenvy;
use std::env;

#[tokio::main]
async fn main() -> Result<(), anyhow::Error> {
    // Load from Master .env (D:\OpenClaw\.env)
    // This must be loaded before accessing env::var()
    let env_path = std::path::Path::new(r"D:\OpenClaw\.env");
    dotenvy::from_filename(env_path).ok();

    println!("🦞 [OpenCLAW] Master .env loaded from: {}", env_path.display());

    // Get DATABASE_URL from Master .env
    let database_url = env::var("DATABASE_URL")
        .unwrap_or_else(|_| "postgres://postgres:2903@localhost:5432/openclaw_db".to_string());

    println!("🌐 [Rust-DB] Connecting to PostgreSQL...");
    println!("📍 Database URL: {}", database_url);

    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await?;

    println!("✅ [Rust-DB] Connection Successful!");

    // Initialize the table
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

    println!("📊 [Rust-DB] 'agent_memory' table ready.");

    // Insert test data if table was newly created
    let count: (i64,) = sqlx::query_as("SELECT COUNT(*) FROM agent_memory")
        .fetch_one(&pool)
        .await?;

    if count.0 == 0 {
        println!("📝 [Rust-DB] Inserting initial record...");
        sqlx::query(
            "INSERT INTO agent_memory (agent_name, content) VALUES ($1, $2)"
        )
        .bind("jayhomebot")
        .bind("System initialized with Master .env configuration")
        .execute(&pool)
        .await?;
    }

    let row: (i64,) = sqlx::query_as("SELECT COUNT(*) FROM agent_memory")
        .fetch_one(&pool)
        .await?;

    println!("✅ [Rust-DB] Connection Successful!");
    println!("📈 [Rust-DB] Total memories stored: {}", row.0);

    Ok(())
}
