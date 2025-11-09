using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Petshop.Migrations
{
    /// <inheritdoc />
    public partial class bdatualizado : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Animais_Planos_PlanoId",
                table: "Animais");

            migrationBuilder.DropColumn(
                name: "Idade",
                table: "Animais");

            migrationBuilder.AlterColumn<int>(
                name: "PlanoId",
                table: "Animais",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AddColumn<DateTime>(
                name: "DataNascimento",
                table: "Animais",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddForeignKey(
                name: "FK_Animais_Planos_PlanoId",
                table: "Animais",
                column: "PlanoId",
                principalTable: "Planos",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Animais_Planos_PlanoId",
                table: "Animais");

            migrationBuilder.DropColumn(
                name: "DataNascimento",
                table: "Animais");

            migrationBuilder.AlterColumn<int>(
                name: "PlanoId",
                table: "Animais",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AddColumn<int>(
                name: "Idade",
                table: "Animais",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddForeignKey(
                name: "FK_Animais_Planos_PlanoId",
                table: "Animais",
                column: "PlanoId",
                principalTable: "Planos",
                principalColumn: "Id");
        }
    }
}
