"""Диалоговое окно для учёта показаний счётчиков."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

import database


class UtilityApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Учёт показаний счётчиков")
        self.geometry("760x620")
        self.minsize(640, 520)

        database.init_database()
        self._build_ui()
        self._refresh_table()

    def _build_ui(self) -> None:
        main = ttk.Frame(self, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        tariffs_frame = ttk.LabelFrame(main, text="Тарифы", padding=10)
        tariffs_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            tariffs_frame,
            text="Формат: ХВС;ГВС;электричество;водоотведение",
        ).pack(anchor=tk.W)
        self.tariffs_entry = ttk.Entry(tariffs_frame, width=80)
        self.tariffs_entry.pack(fill=tk.X, pady=6)
        ttk.Button(tariffs_frame, text="Внести тарифы", command=self._on_set_tariffs).pack(
            anchor=tk.W
        )

        readings_frame = ttk.LabelFrame(main, text="Показания", padding=10)
        readings_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            readings_frame,
            text="Формат: ХВС, ГВС, электричество, месяц",
        ).pack(anchor=tk.W)
        self.readings_entry = ttk.Entry(readings_frame, width=80)
        self.readings_entry.pack(fill=tk.X, pady=6)

        buttons = ttk.Frame(readings_frame)
        buttons.pack(fill=tk.X)
        ttk.Button(buttons, text="Внести показания", command=self._on_add_readings).pack(
            side=tk.LEFT
        )
        ttk.Button(buttons, text="Рассчитать итог", command=self._on_calculate_total).pack(
            side=tk.LEFT, padx=(8, 0)
        )
        ttk.Button(buttons, text="Обновить таблицу", command=self._refresh_table).pack(
            side=tk.LEFT, padx=(8, 0)
        )

        table_frame = ttk.LabelFrame(main, text='Таблица «показания»', padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.table_text = scrolledtext.ScrolledText(
            table_frame,
            wrap=tk.NONE,
            font=("Consolas", 10),
            height=18,
        )
        self.table_text.pack(fill=tk.BOTH, expand=True)
        self.table_text.configure(state=tk.DISABLED)

    def _refresh_table(self) -> None:
        text = database.format_readings_table()
        self.table_text.configure(state=tk.NORMAL)
        self.table_text.delete("1.0", tk.END)
        self.table_text.insert(tk.END, text)
        self.table_text.configure(state=tk.DISABLED)

    def _on_set_tariffs(self) -> None:
        raw = self.tariffs_entry.get().strip()
        if not raw:
            messagebox.showwarning("Тарифы", "Введите значения тарифов.")
            return
        try:
            tariffs = database.set_tariffs(raw)
            messagebox.showinfo(
                "Тарифы сохранены",
                (
                    f"ХВС: {tariffs.hvs}\n"
                    f"ГВС: {tariffs.gvs}\n"
                    f"Электричество: {tariffs.electricity}\n"
                    f"Водоотведение: {tariffs.water_disposal}"
                ),
            )
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _on_add_readings(self) -> None:
        raw = self.readings_entry.get().strip()
        if not raw:
            messagebox.showwarning("Показания", "Введите показания счётчиков.")
            return
        try:
            reading = database.add_readings(raw)
            messagebox.showinfo(
                "Показания сохранены",
                (
                    f"Месяц: {reading.month}\n"
                    f"ХВС: {reading.hvs:g}\n"
                    f"ГВС: {reading.gvs:g}\n"
                    f"Электричество: {reading.electricity:g}"
                ),
            )
            self.readings_entry.delete(0, tk.END)
            self._refresh_table()
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _on_calculate_total(self) -> None:
        try:
            reading, total = database.calculate_total()
            messagebox.showinfo(
                "Расчёт выполнен",
                (
                    f"Месяц: {reading.month}\n"
                    f"Водоотведение (объём): {reading.water_disposal:g}\n"
                    f"Итог к оплате: {total:.2f} руб."
                ),
            )
            self._refresh_table()
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))


def main() -> None:
    app = UtilityApp()
    app.mainloop()


if __name__ == "__main__":
    main()
