using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Petshop.Migrations
{
    /// <inheritdoc />
    public partial class funcionaporfavor : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Planos_Clientes_ClienteId",
                table: "Planos");

            migrationBuilder.DropIndex(
                name: "IX_Planos_ClienteId",
                table: "Planos");

            migrationBuilder.DropColumn(
                name: "ClienteId",
                table: "Planos");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "ClienteId",
                table: "Planos",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.CreateTable(
                name: "Servicos",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Descricao = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Nome = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Servicos", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "PlanosServicos",
                columns: table => new
                {
                    PlanoId = table.Column<int>(type: "int", nullable: false),
                    ServicoId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_PlanosServicos", x => new { x.PlanoId, x.ServicoId });
                    table.ForeignKey(
                        name: "FK_PlanosServicos_Planos_PlanoId",
                        column: x => x.PlanoId,
                        principalTable: "Planos",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_PlanosServicos_Servicos_ServicoId",
                        column: x => x.ServicoId,
                        principalTable: "Servicos",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_Planos_ClienteId",
                table: "Planos",
                column: "ClienteId");

            migrationBuilder.CreateIndex(
                name: "IX_PlanosServicos_ServicoId",
                table: "PlanosServicos",
                column: "ServicoId");

            migrationBuilder.AddForeignKey(
                name: "FK_Planos_Clientes_ClienteId",
                table: "Planos",
                column: "ClienteId",
                principalTable: "Clientes",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
