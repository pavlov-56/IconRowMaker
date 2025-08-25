Icon Row Maker
· python
        state["files"] = list(paths)
        lst.delete(0, tk.END)
        for p in state["files"]:
            lst.insert(tk.END, p)
        lbl_count.config(text=f"Выбрано файлов: {len(state['files'])}")


    def ask_bg():
        # Простой выбор между прозрачным и белым для удобства
        win = tk.Toplevel(root)
        win.title("Фон результата")
        tk.Label(win, text="Выберите фон результата").pack(pady=8)
        def set_transparent():
            state["bg"] = (0,0,0,0)
            win.destroy()
        def set_white():
            state["bg"] = (255,255,255,255)
            win.destroy()
        tk.Button(win, text="Прозрачный", command=set_transparent).pack(fill=tk.X, padx=12, pady=6)
        tk.Button(win, text="Белый", command=set_white).pack(fill=tk.X, padx=12, pady=6)


    def build():
        files = state["files"]
        if not files:
            messagebox.showwarning("Нет файлов", "Сначала добавьте иконки")
            return
        size = state["size"].get()
        spacing = state["spacing"].get()
        try:
            imgs = [load_and_fit(p, size, state["bg"]) for p in files]
            out = compose_row(imgs, size, spacing, state["bg"]) 
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return
        save_to = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", ".png")], title="Сохранить как")
        if not save_to:
            return
        try:
            save_png(out, save_to)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))
            return
        messagebox.showinfo("Готово", f"Сохранено: {save_to}")


    frm_top = tk.Frame(root)
    frm_top.pack(fill=tk.X, padx=12, pady=10)


    tk.Button(frm_top, text="Добавить файлы…", command=pick_files).pack(side=tk.LEFT)
    tk.Button(frm_top, text="Фон…", command=ask_bg).pack(side=tk.LEFT, padx=8)


    tk.Label(frm_top, text="Размер иконки, px:").pack(side=tk.LEFT, padx=(16,4))
    tk.Spinbox(frm_top, textvariable=state["size"], from_=8, to=1024, width=6).pack(side=tk.LEFT)


    tk.Label(frm_top, text="Зазор, px:").pack(side=tk.LEFT, padx=(16,4))
    tk.Spinbox(frm_top, textvariable=state["spacing"], from_=0, to=256, width=6).pack(side=tk.LEFT)


    lbl_count = tk.Label(root, text="Выбрано файлов: 0")
    lbl_count.pack(anchor="w", padx=12)


    lst = tk.Listbox(root, height=12)
    lst.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)


    frm_bottom = tk.Frame(root)
    frm_bottom.pack(fill=tk.X, padx=12, pady=8)
    tk.Button(frm_bottom, text="Собрать и сохранить", command=build).pack(side=tk.RIGHT)


    root.mainloop()
    return 0




def main(argv: List[str] | None = None) -> int:
    ns = parse_args(argv or sys.argv[1:])
    return run_cli(ns)




if __name__ == "__main__":
    raise SystemExit(main())
